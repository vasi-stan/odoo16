/** @odoo-module **/

import { Component, xml, useState, useRef, onMounted } from "@odoo/owl";
import { Counter } from "./counter";
import { TodoList } from "./todolist";
import { Card } from "./card";

export class Playground extends Component {
    static template = "owl_playground.playground";

    static components = {Counter, TodoList, Card};

    countId;
    inputRef = useRef("someInput");

    setup() {
        this.state = useState({
        name:"",
        done:false})
        this.todos = useState([])
    }

    addTodo(ev){
        if (ev.keyCode === 13){
            if (this.state.name != "") {
                this.countId = this.todos.length + 1;
                this.todos.push({
                id:this.countId,
                description: this.state.name,
                done: false});
                this.state.name = "";

            }
        }
    }

    removeTodo(todo) {
        const index = this.todos.findIndex((elem) => elem.id === todo.id);
        this.todos.splice(index, 1)
    }

}





