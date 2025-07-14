<script setup>
// import PieChart from './components/PieChart'
// import DeviceTable from '@/components/DeviceTable'
// import DatabasesTable from '@/components/DatabasesTable'
import TodoList from './components/TodoList'
</script>

<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="24">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <TodoList />
        </div>
      </el-col>

      <!--      <el-col :xs="24" :sm="24" :lg="8">-->
      <!--        <div class="chart-wrapper">-->
      <!--          <PieChart />-->
      <!--        </div>-->
      <!--      </el-col>-->

      <!--      <el-col :xs="24" :sm="24" :lg="8">-->
      <!--        <div class="chart-wrapper">-->
      <!--          <DeviceTable />-->
      <!--        </div>-->
      <!--      </el-col>-->

      <!--      <el-col :xs="24" :sm="24" :lg="8">-->
      <!--        <div class="chart-wrapper">-->
      <!--          <DatabasesTable />-->
      <!--        </div>-->
      <!--      </el-col>-->
    </el-row>
  </div>
</template>

<style scoped lang="scss">
.dashboard-editor-container {
  padding: 20px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

//.flex-parent {
//  display: flex;
//  flex-wrap: wrap;
//}
//
//.flex-parent > * {
//  flex: 1 1 auto;
//}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
