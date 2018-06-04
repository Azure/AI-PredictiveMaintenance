package com.microsoft.ciqs.predictivemaintenance

import java.sql.Timestamp
import java.util.Date
import com.microsoft.azure.storage.table.TableServiceEntity

object Definitions {
  type DeviceId = String

  case class CycleInterval(cycle_start: Timestamp, cycle_end: Timestamp, machineID: DeviceId)

  case class CycleAggregates(val cycle_start: Timestamp,
                             var cycle_end: Timestamp,
                             val machineID: String,
                             var speed_desired_max: Double,
                             var speed_avg: Double,
                             var temperature_avg: Double,
                             var temperature_max: Double,
                             var pressure_avg: Double,
                             var pressure_max: Double) extends  TableServiceEntity {

    private var cycleEnd = cycle_end.toString

    def getspeed_desired_max: Double = speed_desired_max
    def setspeed_desired_max(value: Double): Unit = speed_desired_max = value
    def getcycle_end = cycleEnd
    def setcycle_end(value: String): Unit = cycleEnd = value

    partitionKey = machineID
    rowKey = cycle_start.toString
  }

  case class Signal(timestamp: Timestamp, speed: Double, machineID: DeviceId)
}
