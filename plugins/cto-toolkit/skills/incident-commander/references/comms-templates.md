# Incident comms templates

Plain words, no blame, no speculation. Always say when the next update comes.

## Internal update (channel or email)

```
[SEV<n>] <one-line description>, update <#>
Impact: <who and what is affected, since HH:MM UTC>
Status: investigating | identified | mitigating | monitoring | resolved
What we know: <1–3 facts>
What we're doing: <current action and owner>
Next update: HH:MM UTC
IC: <name>
```

## Status page

```
<Service> is <degraded / unavailable> for <some / all> customers
We're investigating reports of <symptom> since HH:MM UTC. <What customers can do meanwhile, if anything.>
Next update by HH:MM UTC.
```

## Customer email (SEV1 with significant impact)

```
Subject: <Service> disruption on <date>: <resolved / ongoing>

<What happened, in one paragraph, in customer terms.>
<Who was affected and for how long.>
<What we did, and what we're doing so it doesn't happen again.>
<What, if anything, the customer needs to do.>
We're sorry for the disruption.
```

## All-clear

```
[RESOLVED] <one-line description>
Impact: <who and what> from HH:MM to HH:MM UTC (<duration>)
Resolution: <what fixed it>
Follow-up: postmortem on <date>; any permanent fixes are tracked there.
```
