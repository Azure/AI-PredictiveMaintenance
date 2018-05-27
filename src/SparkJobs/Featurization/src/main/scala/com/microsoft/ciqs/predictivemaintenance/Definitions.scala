package com.microsoft.ciqs.predictivemaintenance

import java.sql.Timestamp

object Definitions {
  type DeviceId = String

  case class CycleState(cycle_start: Timestamp, cycle_end: Timestamp, deviceId: DeviceId)

  case class CycleInterval(cycle_start: Timestamp, cycle_end: Timestamp, deviceId: DeviceId)

  case class Signal(timestamp: Timestamp, speed: Double, deviceId: DeviceId)

}
