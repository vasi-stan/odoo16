/** @odoo-module **/

import { Component, xml } from "@odoo/owl";



export class Todo extends Component {
    static props = ['todo','onDelete'];


    static template = xml`<div>
    <p t-attf-class="#{props.todo.done ? 'text-decoration-line-through' : 'text-muted'}">
    <input t-att-checked="props.todo.done" t-att-id="props.todo.id" t-on-click="toggleState" class="form-check-input" type="checkbox" /> <t t-esc="props.todo.id"/>. <t t-esc="props.todo.description"/> <span t-on-click="removeTodo" class="fa fa-remove"/></p>
    </div>`;

    toggleState() {
        this.props.todo.done = !this.props.todo.done
    }

    removeTodo() {
        this.props.onDelete(this.props.todo)
    }
}