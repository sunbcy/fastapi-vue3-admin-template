<template>
  <section class="todoapp">
    <!-- header -->
    <header class="header">
      <input
        class="new-todo"
        autocomplete="off"
        placeholder="Todo List"
        @keyup.enter="addTodo"
        v-model="newTodoText"
      />
    </header>

    <!-- main section -->
    <section v-show="todos?.length" class="main">
      <input
        id="toggle-all"
        :checked="allChecked"
        class="toggle-all"
        type="checkbox"
        @change="toggleAll(!allChecked)"
      />
      <label for="toggle-all" />
      <ul class="todo-list">
        <Todo
          v-for="todo in filteredTodos"
          :key="todo.id"
          :todo="todo"
          @toggle-todo="toggleTodo"
          @edit-todo="editTodo"
          @delete-todo="deleteTodo"
        />
      </ul>
    </section>

    <!-- footer -->
    <footer v-show="todos?.length" class="footer">
      <span class="todo-count">
        <strong>{{ remaining }}</strong>
        {{ pluralize(remaining, 'item') }} left
      </span>
      <ul class="filters">
        <li v-for="(_, key) in filters" :key="key">
          <a
            :class="{ selected: visibility === key }"
            @click.prevent="visibility = key"
          >
            {{ capitalize(key) }}
          </a>
        </li>
      </ul>
      <!-- <button 
        class="clear-completed" 
        v-show="todos.length > remaining" 
        @click="clearCompleted"
      >
        Clear completed
      </button> -->
    </footer>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Todo from './Todo.vue'
import { read_todos, write_todos } from '@/api/todo'

// 数据定义
const visibility = ref('active')
const newTodoText = ref('')
const todos = ref([])

// 筛选器
const filters = {
  all: (todos) => todos,
  active: (todos) => todos.value?.filter((todo) => !todo.done) ?? [],
  completed: (todos) => todos.value?.filter((todo) => todo.done) ?? []
}

// 计算属性
const allChecked = computed(() => {
  return todos.value?.every((todo) => todo.done) ?? false
})

const filteredTodos = computed(() => {
  return filters[visibility.value](todos)
})

const remaining = computed(() => {
  return todos.value?.filter((todo) => !todo.done).length ?? 0
})

// 工具函数
const pluralize = (n, word) => (n === 1 ? word : `${word}s`)
const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1)

// 生命周期钩子
onMounted(async () => {
  await import_todos()
})

// 方法
async function import_todos() {
  try {
    const res = await read_todos()
    todos.value = res.result
  } catch (err) {
    console.error('服务端异常:', err)
  }
}

function setLocalStorage() {
  localStorage.setItem('todos', JSON.stringify(todos.value))
}

async function addTodo(e) {
  const text = newTodoText.value.trim()
  if (!text) return

  const newId =
    todos.value.length > 0 ? Math.max(...todos.value.map((t) => t.id)) + 1 : 1

  const newTodo = {
    id: newId,
    text,
    done: false
  }

  // 保存临时状态以便回滚
  const originalTodos = [...todos.value]

  try {
    // 更新前端状态
    todos.value.push(newTodo)
    newTodoText.value = ''
    setLocalStorage()

    // 发送到后端
    const params = { new_todos: todos.value }
    await write_todos(params)
  } catch (err) {
    console.error('写入失败:', err)
    todos.value = originalTodos // 回滚状态
    setLocalStorage()
  }
}

function toggleTodo(todo) {
  todo.done = !todo.done
  setLocalStorage()

  // 如果需要，可以在此添加API调用以保存状态
}

function deleteTodo(todo) {
  const index = todos.value.findIndex((t) => t.id === todo.id)
  if (index !== -1) {
    todos.value.splice(index, 1)
    setLocalStorage()

    // 如果需要，可以在此添加API调用以保存状态
  }
}

function editTodo({ todo, value }) {
  if (todo) {
    todo.text = value
    setLocalStorage()
  }
}

function clearCompleted() {
  todos.value = todos.value.filter((todo) => !todo.done)
  setLocalStorage()
}

function toggleAll(done) {
  todos.value.forEach((todo) => {
    todo.done = done
  })
  setLocalStorage()
}
</script>

<style lang="scss">
.todoapp {
  background: #fff;
  margin: 20px 0 40px 0;
  position: relative;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 25px 50px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;

  .header {
    padding: 15px 16px 16px;
    border-bottom: 1px solid #ededed;

    .new-todo {
      position: relative;
      width: 100%;
      font-size: 24px;
      font-family: inherit;
      font-weight: inherit;
      line-height: 1.4em;
      padding: 6px;
      border: 1px solid #999;
      box-shadow: inset 0 -1px 5px 0 rgba(0, 0, 0, 0.2);
      box-sizing: border-box;
      border-radius: 4px;

      &::placeholder {
        font-style: italic;
        font-weight: 300;
        color: #e6e6e6;
      }
    }
  }

  .main {
    position: relative;
    z-index: 2;
    border-top: 1px solid #e6e6e6;
    padding: 20px;

    .toggle-all {
      position: absolute;
      top: 22px;
      left: -10px;
      width: 40px;
      height: 40px;
      text-align: center;
      border: none;
      opacity: 0;
      cursor: pointer;

      & + label {
        width: 40px;
        height: 40px;
        font-size: 0;
        position: absolute;
        top: 22px;
        left: -10px;

        &:before {
          content: '❯';
          font-size: 22px;
          color: #e6e6e6;
          padding: 10px 15px;
          transform: rotate(90deg);
        }
      }

      &:checked + label:before {
        color: #737373;
      }
    }

    .todo-list {
      margin: 0;
      padding: 0;
      list-style: none;
    }
  }

  .footer {
    color: #777;
    padding: 10px 15px;
    height: 40px;
    text-align: center;
    border-top: 1px solid #e6e6e6;

    .todo-count {
      float: left;
      text-align: left;

      strong {
        font-weight: 300;
      }
    }

    .filters {
      margin: 0;
      padding: 0;
      list-style: none;
      position: absolute;
      left: 0;
      right: 0;

      li {
        display: inline;

        a {
          color: inherit;
          margin: 3px;
          padding: 3px 7px;
          text-decoration: none;
          border: 1px solid transparent;
          border-radius: 3px;

          &:hover {
            border-color: rgba(175, 47, 47, 0.1);
          }

          &.selected {
            border-color: rgba(175, 47, 47, 0.2);
          }
        }
      }
    }

    .clear-completed {
      float: right;
      position: relative;
      line-height: 20px;
      text-decoration: none;
      cursor: pointer;
      background: none;
      border: none;
      color: #777;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}
</style>
