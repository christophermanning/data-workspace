---
draft: true
---

# Index

### Pages

[amtrak-stations-near-bikeshare.md](/amtrak-stations-near-bikeshare/)

### Services

```js
const services = FileAttachment("/data/services.json").json();
```
${html`<ul>${Object.keys(services).map(d => { return html`<li><a href="${services[d]}">${d}</a></li>`})}</ul>`}
