/** @odoo-module **/

import { Component, xml, useState, useEffect, useRef, onMounted } from "@odoo/owl";

export class Utils extends Component {
    static props = ['inputRef'];

    setup() {
        useAutofocus("props.inputRef");
    }
}

function useAutofocus(name) {
    let ref = useRef(name);
    useEffect(
    (el) => el && el.focus(),
    () => [ref.el]
    );
}