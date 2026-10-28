# Receipt-boundary source review

The completed-operation branch also requires the already recorded
reply_before_deadline flag. Otherwise an IO/timer scheduling race could choose
a ready operation after the deadline. This preserves the stated receipt
boundary on both operation-complete and retirement-interrupted paths. No
request time is increased. The existing late-reply/cancellation/malformed
controls remain applicable; this is a forward source correction after a750aa3,
not a rewrite of that commit or its CI result.
