## Branch Strategy

- `main` is the stable integration branch.
- Direct push to `main` is not allowed.
- All changes shall be merged through Pull Requests.
- Working branches shall be created from `main`.

Branch naming:

- `dev/(issue-id)-<short-description>`
- `docs/(issue-id)-<short-description>`

## Commit Message Rule
(#<issue-no>) <summary> 
(#12) add cmake hardware target selection 
(#18) handle null display backend 
(#21) update architecture overview 
(#24) add config parser unit tests 

## Merge Rule

- Use Pull Request only.
- Prefer Squash Merge to keep `main` history clean.
- Delete branch after merge.
- Each PR shall be linked to at least one GitHub Issue.
