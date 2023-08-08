/** @odoo-module **/

import { Component, xml, useState, useRef, onMounted } from "@odoo/owl";

import { Todo } from "./todo";

export class TodoList extends Component {
    static props = ['todos','onDelete'];
    static components = {Todo};

    static template = xml`<div>
        <t t-foreach="props.todos" t-as="todolist" t-key="todolist.id">
            <Todo todo="todolist" onDelete.bind="removeTodo"/>
        </t>
    </div>`;

    removeTodo(todo) {
        this.props.onDelete(todo)
    }

}

