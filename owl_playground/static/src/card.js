/** @odoo-module **/

import { Component, xml, useState, useRef, onMounted } from "@odoo/owl";

export class Card extends Component {
    static template = xml`<div>
        <t t-set-slot="title">Card title</t>
        <t t-set-slot="content">
            <p class="card-text">Some quick example text...</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
        </t>
    </div>`;
}