<template>
  <main>
    <header>
      <strong>Workflow Studio</strong>
      <el-button @click="s.saveWorkflow">Save</el-button><el-button @click="s.validateWorkflow">Validate</el-button><el-button @click="run">Run</el-button><el-button @click="s.publishWorkflow">Publish</el-button>
      <el-divider direction="vertical"/><el-button @click="s.copyNode">Copy</el-button><el-button @click="s.autoLayout">Auto layout</el-button><el-button @click="s.undo">Undo</el-button><el-button @click="s.redo">Redo</el-button>
      <el-dropdown><el-button>Export</el-button><template #dropdown><el-dropdown-menu><el-dropdown-item @click="download('workflow.json',JSON.stringify(s.dsl(),null,2))">Workflow JSON</el-dropdown-item><el-dropdown-item @click="exportPython">Python</el-dropdown-item></el-dropdown-menu></template></el-dropdown>
      <el-dropdown><el-button>Import</el-button><template #dropdown><el-dropdown-menu><el-dropdown-item @click="importJson">Workflow JSON</el-dropdown-item><el-dropdown-item @click="importPython">Python</el-dropdown-item></el-dropdown-menu></template></el-dropdown>
    </header>
    <div class="work"><NodePalette @add="add"/><WorkflowCanvas/><PropertiesPanel/></div><DebugPanel/>
  </main>
</template>
<script setup lang="ts">
import{onMounted,onUnmounted}from'vue';import{ElMessageBox}from'element-plus';import{useWorkflowStore}from'../stores/workflow';import{useRuntimeStore}from'../stores/runtime';import{api}from'../api/client';import NodePalette from '../components/canvas/NodePalette.vue';import WorkflowCanvas from '../components/canvas/WorkflowCanvas.vue';import PropertiesPanel from '../components/panels/PropertiesPanel.vue';import DebugPanel from '../components/panels/DebugPanel.vue';
const s=useWorkflowStore(),r=useRuntimeStore();const add=(type:any)=>s.addNode(type);const run=async()=>{const x=await s.runWorkflow('');r.connect(x.data.run_id,x.data.trace_id)};const download=(name:string,data:string)=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([data],{type:'text/plain'}));a.download=name;a.click();URL.revokeObjectURL(a.href)};const exportPython=async()=>{if(!s.workflowId)return download('workflow.py','# Save this workflow before exporting Python.');const x=await api.get(`/api/workflows/${s.workflowId}/export/python`);download('workflow.py',x.data.source)};const importJson=async()=>{const x=await ElMessageBox.prompt('Paste Workflow JSON','Import Workflow');s.importDsl(JSON.parse(x.value))};const importPython=async()=>{const x=await ElMessageBox.prompt('Paste Workflow Studio Python','Import Python',{inputType:'textarea'});const result=await api.post('/api/workflows/import/python',{source:x.value});s.importDsl(result.data)};const key=(e:KeyboardEvent)=>{if(e.ctrlKey&&e.key==='z')s.undo();if(e.ctrlKey&&e.key==='y')s.redo()};onMounted(()=>addEventListener('keydown',key));onUnmounted(()=>removeEventListener('keydown',key));

</script>
<style scoped>main{height:100%;display:flex;flex-direction:column}header{padding:8px;border-bottom:1px solid #ddd;display:flex;gap:7px;align-items:center}.work{display:flex;flex:1;min-height:0}.work>:nth-child(2){flex:1}</style>
