package com.microsoft.ciqs.predictivemaintenance

import java.sql.Timestamp
import org.scalatest.FunSuite

class CycleAggregatorTests extends FunSuite {
  val MS = 1000

  test("getIntervalsFromTimeSeries returns one interval for contiguous timestamps") {
    val series = (1 to 10).map(t => new Timestamp(t * MS))
    val first = series.head
    val last = series.last
    val intervals = CycleAggregator.getIntervalsFromTimeSeries(series.iterator, CycleAggregator.DEFAULT_CYCLE_GAP_MS)
    assert(intervals.length === 1)

    val interval = intervals.head

    assert(interval(0).getTime === first.getTime)
    assert(interval(1).getTime === last.getTime)
  }

  test("getIntervalsFromTimeSeries returns one interval for timestamps with small gaps") {
    val series = (1 to 100 by 10).map(t => new Timestamp(t * MS))
    val first = series.head
    val last = series.last
    val intervals = CycleAggregator.getIntervalsFromTimeSeries(series.iterator, CycleAggregator.DEFAULT_CYCLE_GAP_MS)
    assert(intervals.length === 1)

    val interval = intervals.head

    assert(interval(0).getTime === first.getTime)
    assert(interval(1).getTime === last.getTime)
  }

  test("getIntervalsFromTimeSeries returns two intervals") {
    val series1 = (1 to 100).map(t => new Timestamp(t * MS))
    val firstStart = series1.head
    val firstEnd = series1.last

    val series2 = (1 to 100).map(t => new Timestamp((t + 100) * MS + CycleAggregator.DEFAULT_CYCLE_GAP_MS))
    val secondStart = series2.head
    val secondEnd = series2.last

    val series = series1 ++ series2

    val intervals = CycleAggregator.getIntervalsFromTimeSeries(series.iterator, CycleAggregator.DEFAULT_CYCLE_GAP_MS)
    assert(intervals.length === 2)

    // intervals are returned in a reverse order
    assert(intervals(1)(0) === firstStart)
    assert(intervals(1)(1) === firstEnd)
    assert(intervals(0)(0) === secondStart)
    assert(intervals(0)(1) === secondEnd)
  }
}
