//! Linux startup defaults from process eligibility and visible cgroup v2 ancestors.
use std::{
    io,
    path::{Path, PathBuf},
};

fn read_optional(path: &Path) -> io::Result<Option<String>> {
    match std::fs::read_to_string(path) {
        Ok(text) => Ok(Some(text)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(e),
    }
}
fn cgroups() -> io::Result<Vec<PathBuf>> {
    let membership = std::fs::read_to_string("/proc/self/cgroup")?;
    let current = membership.lines().find_map(|l| l.strip_prefix("0::"));
    let mounts = std::fs::read_to_string("/proc/self/mountinfo")?;
    for line in mounts.lines() {
        let Some((left, _)) = line.split_once(" - cgroup2 ") else {
            continue;
        };
        let fields: Vec<_> = left.split_whitespace().collect();
        let unescape = |s: &str| {
            s.replace("\\040", " ")
                .replace("\\011", "\t")
                .replace("\\134", "\\")
        };
        let root = PathBuf::from(unescape(fields[3]));
        let mount = PathBuf::from(unescape(fields[4]));
        let current = PathBuf::from(current.unwrap_or("/"));
        let relative = current.strip_prefix(&root).map_err(io::Error::other)?;
        if relative
            .components()
            .any(|c| !matches!(c, std::path::Component::Normal(_)))
        {
            return Err(io::Error::other("invalid cgroup membership"));
        }
        return Ok(mount
            .join(relative)
            .ancestors()
            .take_while(|p| p.starts_with(&mount))
            .map(Path::to_path_buf)
            .collect());
    }
    Ok(vec![])
}
fn quota(text: &str) -> io::Result<Option<usize>> {
    let mut words = text.split_whitespace();
    let first = words
        .next()
        .ok_or_else(|| io::Error::other("missing CPU quota"))?;
    if first == "max" {
        return Ok(None);
    }
    let q: u64 = first.parse().map_err(io::Error::other)?;
    let p: u64 = words
        .next()
        .ok_or_else(|| io::Error::other("missing CPU period"))?
        .parse()
        .map_err(io::Error::other)?;
    if p == 0 {
        return Err(io::Error::other("zero CPU period"));
    }
    Ok(Some((q / p).max(1).min(usize::MAX as u64) as usize))
}
pub fn cpus(eligible: Vec<usize>) -> io::Result<Vec<usize>> {
    let mut count = eligible.len();
    for group in cgroups()? {
        if let Some(text) = read_optional(&group.join("cpu.max"))?
            && let Some(limit) = quota(&text)?
        {
            count = count.min(limit);
        }
    }
    Ok(eligible.into_iter().take(count).collect())
}
fn mem_available(text: &str) -> io::Result<u64> {
    text.lines()
        .find_map(|l| l.strip_prefix("MemAvailable:"))
        .and_then(|s| s.split_whitespace().next())
        .ok_or_else(|| io::Error::other("MemAvailable unavailable"))?
        .parse::<u64>()
        .map_err(io::Error::other)?
        .checked_mul(1024)
        .ok_or_else(|| io::Error::other("memory size overflow"))
}
fn remaining(maximum: &str, current: &str) -> io::Result<Option<u64>> {
    if maximum.trim() == "max" {
        return Ok(None);
    }
    let limit: u64 = maximum.trim().parse().map_err(io::Error::other)?;
    let used: u64 = current.trim().parse().map_err(io::Error::other)?;
    Ok(Some(limit.saturating_sub(used)))
}
pub fn memory_bytes() -> io::Result<u64> {
    let mut free = mem_available(&std::fs::read_to_string("/proc/meminfo")?)?;
    for group in cgroups()? {
        if let Some(maximum) = read_optional(&group.join("memory.max"))? {
            let current = std::fs::read_to_string(group.join("memory.current"))?;
            if let Some(room) = remaining(&maximum, &current)? {
                free = free.min(room);
            }
        }
    }
    // Leave 20% of currently available capacity for the host/container's other work.
    let budget = free / 5 * 4;
    if budget == 0 {
        return Err(io::Error::other("no available memory for verification"));
    }
    Ok(budget)
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn quota_fraction_does_not_oversubscribe() {
        assert_eq!(quota("150000 100000").unwrap(), Some(1));
        assert_eq!(quota("50000 100000").unwrap(), Some(1));
        assert_eq!(quota("max 100000").unwrap(), None);
        assert!(quota("1 0").is_err());
    }
    #[test]
    fn available_not_physical_or_swap() {
        assert_eq!(
            mem_available("MemTotal: 999999 kB\nMemAvailable: 1024 kB\nSwapFree: 9999 kB").unwrap(),
            1048576
        );
        assert!(mem_available("MemTotal: 999999 kB").is_err());
    }
    #[test]
    fn container_pressure_reduces_budget() {
        assert_eq!(remaining("100", "80").unwrap(), Some(20));
        assert_eq!(remaining("100", "120").unwrap(), Some(0));
        assert_eq!(remaining("max", "80").unwrap(), None);
    }
}
