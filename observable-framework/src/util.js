import {html} from "npm:htl";

export function link(name, url, title="") {
  return html`<a href="${url}" title=" ${title}" rel="noopener noreferrer nofollow" target="_blank">${name}</a>`
}

export function citation(title, url, source, date) {
  return html`${link(title, url)} <i>${source}</i> ${date}`
}
