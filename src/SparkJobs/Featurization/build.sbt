name := "Featurizer"
version := "1.0"
scalaVersion := "2.11.8"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "2.3.0",
  "org.apache.spark" %% "spark-streaming" % "2.3.0",
  "org.apache.spark" %% "spark-sql" % "2.3.0",
  "com.microsoft.azure" %% "azure-eventhubs-spark" % "2.3.1",
  "com.microsoft.azure" % "azure-storage" % "7.0.0"
)

libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.5" % "test"
