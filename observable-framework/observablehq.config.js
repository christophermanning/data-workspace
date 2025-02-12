// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "Workspace",

  // Content to add to the head of the page, e.g. for a favicon:
  head: '',

  // The path to the source root.
  root: "src",

  // don't load google fonts
  globalStylesheets: [],

  style: ["embed.css"],

  footer: () => {
    let date = new Date().toLocaleString("en-US", {timeZoneName: "short"})
    return `
<div class="small">
<p>
<b>Created By</b> <a href="https://www.christophermanning.net" target="_blank">Christopher Manning</a> |
<b>Source Code</b> <a href="https://github.com/christophermanning/data-workspace/tree/main/observable-framework" target="_blank">GitHub</a>
</p>
Built with <a href="https://observablehq.com/" target="_blank">Observable</a> on <a title="${date}">${date}</a>.
</div>
  `}, // what to show in the footer (HTML)
  sidebar: false, // whether to show the sidebar
  toc: false, // whether to show the table of contents
  // pager: false, // whether to show previous & next links in the footer
  // output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // cleanUrls: true, // drop .html from URLs
};
