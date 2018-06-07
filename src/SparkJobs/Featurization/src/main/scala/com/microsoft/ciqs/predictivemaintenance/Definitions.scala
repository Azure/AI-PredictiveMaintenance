package com.microsoft.ciqs.predictivemaintenance

import java.sql.Timestamp
import com.microsoft.azure.storage.table.TableServiceEntity

object Definitions {
  type DeviceId = String

  case class CycleInterval(start: Timestamp, end: Timestamp, machineID: DeviceId)

  case class CycleAggregates(val cycle_start: Timestamp,
                             var cycle_end: Timestamp,
                             val machineID: String,
                             var speed_desired_max: Double,
                             var speed_avg: Double,
                             var temperature_avg: Double,
                             var temperature_max: Double,
                             var pressure_avg: Double,
                             var pressure_max: Double,
                             var raw_count: Long) extends  TableServiceEntity {

    private var cycleEnd = cycle_end.toString

    def getcycle_end = cycleEnd
    def setcycle_end(value: String): Unit = cycleEnd = value

    def getspeed_desired_max: Double = speed_desired_max
    def setspeed_desired_max(value: Double): Unit = speed_desired_max = value

    def getspeed_avg: Double = speed_avg
    def setspeed_avg(value: Double): Unit = speed_avg = value

    def gettemperature_avg: Double = temperature_avg
    def settemperature_avg(value: Double): Unit = temperature_avg = value

    def gettemperature_max: Double = temperature_max
    def settemperature_max(value: Double): Unit = temperature_max = value

    def getpressure_avg: Double = pressure_avg
    def setpressure_avg(value: Double): Unit = pressure_avg = value

    def getpressure_max: Double = pressure_max
    def setpressure_max(value: Double): Unit = pressure_max = value

    def getraw_count: Long = raw_count
    def setraw_count(value: Long): Unit = raw_count = value

    partitionKey = machineID
    rowKey = cycle_start.toString
  }

  case class Signal(timestamp: Timestamp, speed: Double, machineID: DeviceId)
}
