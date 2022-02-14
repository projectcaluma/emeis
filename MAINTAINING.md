# Maintainer's Handbook

## Releasing a new version

Here is a rough outline / checklist for the release (explained further below):

1. Checkout `main` branch, ensure you have all tags
2. Prepare changelog
3. Figure out the next version
4. Update code (CHANGELOG, version info)
5. Pull Request with the version bump.
6. Create tag on the merge commit
7. Upload / edit change log

Here's how this works in detail:

### Get release information

The `semantic-release` tool can help you with the first few tasks of the above
checklist:

```bash
# Ensure you're on the current main and have all release tags
git checkout main
git pull origin --tags

# Prepare changelog
semantic-release changelog --noop --unreleased -D version_source=tag

# Figure out the next version
semantic-release version --noop -D version_source=tag
```

### Update version, changelog in source

The version is also put in code. Update the file
`emeis/emeis_metadata.py`.

Put the changelog on top of the `CHANGELOG.md` file along with the proposed date
of release. If needed, amend it with some informative text about the release.

### Create a Pull request for the proposed version bump

Put the changelog in the commit message or in the PR discussion somewhere, so
it won't be forgotten once the release actually happens.

Note: If other PRs are merged after you create the version bump PR, you may need
to revisit the changelog, and potentially even the version number to be created.
It is thus important to create and merge the version bump in a timely,
coordinated manner.

### Create Release

Once the version bump PR has been merged, take the corresponding merge commit,
and tag it with the version. Note that the tag needs to be prefixed with `v`,
so for example version 5.0.0 will need a tag named exactly `v5.0.0`.

You should then edit the release on Github and paste the changelog there as well.

The `pypi` github workflow will automatically build a source package and a wheel and
publish them on [PyPI](https://pypi.org/project/emeis/).

The `ghcr` github workflow will automatically publish the new docker image on [ghcr.io/projectcaluma/emeis](https://ghcr.io/projectcaluma/emeis).
