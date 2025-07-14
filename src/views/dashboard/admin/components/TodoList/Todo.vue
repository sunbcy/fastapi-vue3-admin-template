<script setup>
import { edit_write_todos, del_todos } from '@/api/todo'
import { nextTick, ref } from 'vue'
import { ElMessage } from 'element-plus'

const name = ref('Todo')
const vFocus = {
  mounted(el, { value }) {
    if (value) nextTick(() => el.focus())
  },
  updated(el, { value, oldValue }) {
    if (value && value !== oldValue) {
      nextTick(() => el.focus())
    }
  }
}

const props = defineProps(['todo'])
// 使用 defineEmits 声明组件事件
const emit = defineEmits(['toggleTodo', 'editTodo', 'deleteTodo'])
const editing = ref(false)

const deleteTodo = async () => {
  emit('deleteTodo', props.todo)
  const text = props.todo.text
  const params = { del_todos: text, del_id: props.todo.id }

  try {
    const res = await del_todos(params)
    ElMessage.success(`成功删除 todos ✅`)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('删除 todos 失败!')
  }
}

const editWriteTodo = async (todo) => {
  const params = { edit_todos: todo.text, edit_id: todo.id }
  try {
    const res = await edit_write_todos(params)
    ElMessage.success(`成功写入new todos✅`)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('写入new todos失败!')
  }
}

const editTodo = async (value) => {
  emit('deleteTodo', { todo: props.todo, value })
}

const toggleTodo = async () => {
  emit('toggleTodo', props.todo)
}

const doneEdit = async (e) => {
  const value = e.target.value.trim()
  const { todo } = this
  if (!value) {
    deleteTodo({
      todo
    })
  } else if (editing.value) {
    editTodo({
      todo,
      value
    })
    editing.value = false
  }
}

const cancelEdit = async (e) => {
  const { todo } = this
  e.target.value = todo.text
  editing.value = false
}
</script>

<template>
  <li :class="{ completed: todo.done, editing: editing }" class="todo">
    <div class="view">
      <input
        :checked="todo.done"
        class="toggle"
        type="checkbox"
        @change="toggleTodo(todo)"
      />
      <label>
        <span
          contenteditable="true"
          class="editable-text"
          @dblclick="editing = true"
          v-text="todo.text"
        />
      </label>
      <button class="destroy" @click="deleteTodo(todo)" />
    </div>
    <input
      v-show="editing"
      v-focus="editing"
      :value="todo.text"
      class="edit"
      @keyup.enter="doneEdit"
      @keyup.esc="cancelEdit"
      @blur="doneEdit"
    />
  </li>
</template>

<style scoped lang="scss">
.editable-text {
  display: inline-block;
  padding: 4px;
}
.editable-text:focus {
  outline: none;
  border: 1px dashed #409eff;
}
</style>
