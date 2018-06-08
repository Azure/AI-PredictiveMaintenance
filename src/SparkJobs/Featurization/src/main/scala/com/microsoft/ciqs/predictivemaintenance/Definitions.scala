package com.microsoft.ciqs.predictivemaintenance

import java.sql.Timestamp
import scala.beans.BeanProperty
import com.microsoft.azure.storage.table.TableServiceEntity

object Definitions {
  case class TelemetryEvent(timestamp: Timestamp, machineID: String)

  case class CycleInterval(start: Timestamp, end: Timestamp, machineID: String)

  case class CycleAggregates(var MachineID: String,
                             var CycleStart: String,
                             @BeanProperty var CycleEnd: String,
                             @BeanProperty var SpeedDesiredMax: Double,
                             @BeanProperty var SpeedAvg: Double,
                             @BeanProperty var TemperatureAvg: Double,
                             @BeanProperty var TemperatureMax: Double,
                             @BeanProperty var PressureAvg: Double,
                             @BeanProperty var PressureMax: Double,
                             @BeanProperty var RawCount: Long) extends  TableServiceEntity {

    // nullary constructor
    def this() {
      this(null, null, null, 0, 0, 0, 0, 0, 0, 0)
    }

    override def setPartitionKey(partitionKey: String): Unit = {
      MachineID = partitionKey
      super.setPartitionKey(partitionKey)
    }

    override def setRowKey(rowKey: String): Unit = {
      CycleStart = rowKey
      super.setRowKey(rowKey)
    }

    partitionKey = MachineID
    rowKey = CycleStart
  }

  case class Features(val MachineID: String,
                      val CycleStart: String,
                      @BeanProperty
                      var CycleEnd: String) extends TableServiceEntity {

    @BeanProperty
    var FeaturesJson: String = null

    partitionKey = MachineID
    rowKey = CycleStart
  }
}
