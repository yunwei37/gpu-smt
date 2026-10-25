//! Linux owned-process accounting. Never enumerate another tree as owned.
use gpu_smt_core::{ProcessIdentity, ProcessSample, ResourceMonitor, ResourceSnapshot};
use std::{
    collections::{HashMap, HashSet},
    fs,
    sync::Mutex,
};

#[derive(Clone)]
struct Stat {
    identity: ProcessIdentity,
    parent: u32,
    rss: u64,
}

fn stat(pid: u32) -> Result<Option<Stat>, String> {
    let raw = match fs::read_to_string(format!("/proc/{pid}/stat")) {
        Ok(s) => s,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),
        Err(e) => return Err(e.to_string()),
    };
    let tail = raw.rsplit_once(')').ok_or("invalid proc stat")?.1;
    let fields: Vec<_> = tail.split_whitespace().collect();
    let n = |i: usize| -> Result<u64, String> {
        fields
            .get(i)
            .ok_or("short proc stat")?
            .parse()
            .map_err(|e| format!("{e}"))
    };
    // SAFETY: sysconf is thread safe and has no pointer arguments.
    let page = unsafe { libc::sysconf(libc::_SC_PAGESIZE) };
    if page <= 0 {
        return Err("cannot discover page size".into());
    }
    Ok(Some(Stat {
        identity: ProcessIdentity {
            pid,
            start_ticks: n(19)?,
        },
        parent: n(1)? as u32,
        rss: n(21)?.saturating_mul(page as u64),
    }))
}

/// Read the actual kernel birth identity; absent processes are not registered.
pub fn identity(pid: u32) -> Result<ProcessIdentity, String> {
    stat(pid)?
        .map(|s| s.identity)
        .ok_or_else(|| format!("process {pid} already exited"))
}

/// Linux /proc RSS, retaining discovered descendants across reparenting.
#[derive(Default)]
pub struct ProcMonitor {
    known: Mutex<HashMap<(u32, u64), Vec<ProcessIdentity>>>,
}
impl ResourceMonitor for ProcMonitor {
    fn sample(&self, roots: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        let mut table = HashMap::new();
        for e in fs::read_dir("/proc").map_err(|e| e.to_string())? {
            let e = e.map_err(|e| e.to_string())?;
            if let Ok(pid) = e.file_name().to_string_lossy().parse::<u32>() {
                // Registered identities below are checked strictly. Unrelated inaccessible
                // processes never become owned and need not be inspected.
                if let Ok(Some(s)) = stat(pid) {
                    table.insert(pid, s);
                }
            }
        }
        let mut accounted_roots = roots.to_vec();
        let own = identity(std::process::id())?;
        if !accounted_roots.contains(&own) {
            accounted_roots.push(own);
        }
        let mut known = self.known.lock().unwrap();
        let wanted: HashSet<_> = accounted_roots
            .iter()
            .map(|r| (r.pid, r.start_ticks))
            .collect();
        known.retain(|k, _| wanted.contains(k));
        let mut seen = HashSet::new();
        let mut result = ResourceSnapshot::default();
        for root in &accounted_roots {
            let key = (root.pid, root.start_ticks);
            let entries = known.entry(key).or_default();
            if let Some(current) = stat(root.pid)?
                && current.identity == *root
                && !entries.contains(root)
            {
                entries.push(root.clone());
            }
            loop {
                let before = entries.len();
                for s in table.values() {
                    if entries.iter().any(|p| {
                        p.pid == s.parent && table.get(&p.pid).is_some_and(|x| x.identity == *p)
                    }) && !entries.contains(&s.identity)
                    {
                        entries.push(s.identity.clone());
                    }
                }
                if entries.len() == before {
                    break;
                }
            }
            let mut rss = 0u64;
            for p in entries.iter() {
                if let Some(s) = stat(p.pid)?
                    && s.identity == *p
                {
                    rss = rss.saturating_add(s.rss);
                    if seen.insert((p.pid, p.start_ticks)) {
                        result.rss_bytes = result.rss_bytes.saturating_add(s.rss);
                    }
                }
            }
            if roots.contains(root) {
                result.processes.push(ProcessSample {
                    identity: root.clone(),
                    rss_bytes: rss,
                });
            }
        }
        if !seen.iter().any(|(pid, _)| *pid == std::process::id())
            && let Some(s) = stat(std::process::id())?
        {
            result.rss_bytes = result.rss_bytes.saturating_add(s.rss);
        }
        Ok(result)
    }
}
