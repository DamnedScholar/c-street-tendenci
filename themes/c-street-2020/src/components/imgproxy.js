import {LitElement, html, css, customElement, property} from 'lit-element';

// TODO: This is incomplete, as the proper functionality for the component is kind of an unnecessary feature for the MVP. I want a smart `picture` tag that has `sources` pointing at a couple of different imgproxy URLs for different sizes, with awareness of `tailwind.config.js` and the ability to determine what size of image to make based on generated width and height utilities. For now, I can just stick plain-HTML `picture` tags in each template that would use this, to establish a working example of the pattern before I go and make it all smart.

// This decorator defines the element.
@customElement('img-proxy')
export class ImgProxy extends LitElement {

    static get properties() {
        return { 
            src: { attribute: "src", type: String },
            proxy_url: { attribute: "proxy-src", type: String, reflect: true },
            proxy_key: { attribute: false, type: String, reflect: true },
            height: { attribute: "height", type: Number },
            width: { attribute: "width", type: Number },
            gravity: { attribute: "gravity", type: String },
            enlarge: { attribute: "enlarge", type: Number }
        };
      }

    static styles = css`
    img {
        
    }`;

    constructor() {
        super();
        this.src = src;
        this.proxy_url = proxy_url;
        this.items = [1, 2, 3];
    }

    // Render element DOM by returning a `lit-html` template.
    render() {
        return html`
            <picture>
                <source srcset="" media="true">
                <img src="" alt="">
            </picture>
        `;
    }

}
