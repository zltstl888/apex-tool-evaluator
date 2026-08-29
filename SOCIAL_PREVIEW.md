# Social Preview provenance

The Social Preview for `v0.1.3` is distributed as a versioned release asset so the repository image used in sharing can be traced to exact bytes. The same image bytes are used in the GitHub repository Social Preview setting.

## Release asset identity

- Release tag: `v0.1.3`
- Asset name: `apex-tool-evaluator-social-preview-v0.1.3.jpg`
- Dimensions: `1280 x 640`
- SHA-256: `baaa5708f6fec725689a436f315a629481f1b6a03b74f5566b592f39f4089780`

## Verification

```bash
gh release download v0.1.3 \
  --repo zltstl888/apex-tool-evaluator \
  --pattern 'apex-tool-evaluator-v0.1.3.skill' \
  --pattern 'apex-tool-evaluator-social-preview-v0.1.3.jpg' \
  --pattern 'SHA256SUMS'
shasum -a 256 -c SHA256SUMS
```

The release asset, checksum manifest, and GitHub Social Preview setting provide a reproducible identity for the public preview.
