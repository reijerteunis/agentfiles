# Deep-merge JSON layers, last layer wins: objects merge key by key, arrays are unioned (order kept,
# no duplicates), scalars are replaced. Usage: jq -s -f merge-settings.jq existing.json base.json [overlay.json]
# Parameters are $values, not filters: filter parameters re-evaluate against the reduce accumulator.
def dmerge($a; $b):
  if ($a | type) == "object" and ($b | type) == "object" then
    reduce ($b | keys_unsorted[]) as $k ($a;
      .[$k] = (if ($a | has($k)) then dmerge($a[$k]; $b[$k]) else $b[$k] end))
  elif ($a | type) == "array" and ($b | type) == "array" then
    reduce $b[] as $item ($a; if any(.[]; . == $item) then . else . + [$item] end)
  else $b end;
reduce .[1:][] as $layer (.[0]; dmerge(.; $layer))
