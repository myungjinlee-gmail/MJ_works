# PlantUML

PlantUML is an optional documentation tool. It is not installed by
`scripts/setup_dev.sh`. A Java runtime, Graphviz, and either `curl` or `wget`
are required.

## Install Java

On the supported Ubuntu 24.04 host, install the OpenJDK 21 headless runtime:

```bash
sudo apt-get update
sudo apt-get install -y openjdk-21-jre-headless
```

Verify that Java is available:

```bash
java -version
```

When more than one Java version is installed, select the Java 21 executable:

```bash
sudo update-alternatives --config java
```

## Install PlantUML

The repository pins PlantUML 1.2026.6. Download the executable JAR from the
official release while in the repository root:

```bash
mkdir -p thirdparty/plantuml
curl -fL \
  https://github.com/plantuml/plantuml/releases/download/v1.2026.6/plantuml.jar \
  -o thirdparty/plantuml/plantuml.jar
```

Verify the downloaded artifact:

```bash
echo "89948f14c93756c7a3fb7b69078ff37e8489fd79dd430c582b931e2f65358690  thirdparty/plantuml/plantuml.jar" \
  | sha256sum --check
```

Check PlantUML:

```bash
java -jar thirdparty/plantuml/plantuml.jar -version
```

## Install Graphviz

PlantUML uses the Graphviz `dot` executable to lay out class, component,
deployment, state, and several other diagram types. Without it, PlantUML can
generate only diagram types that do not require Graphviz, such as sequence
diagrams.

Install Graphviz on Ubuntu 24.04:

```bash
sudo apt-get update
sudo apt-get install -y graphviz
```

Verify the executable and let PlantUML test it:

```bash
dot -V
java -jar thirdparty/plantuml/plantuml.jar -testdot
```

PlantUML normally finds `/usr/bin/dot` automatically. If Graphviz is installed
in another location, set its path explicitly:

```bash
export GRAPHVIZ_DOT="$(command -v dot)"
java -jar thirdparty/plantuml/plantuml.jar -testdot
```

If `dot` exists but reports a plugin configuration problem, rebuild its plugin
configuration and test again:

```bash
sudo dot -c
java -jar thirdparty/plantuml/plantuml.jar -testdot
```

The successful test output should report the Graphviz version and end with
`Installation seems OK`.

Generate SVG files from a PlantUML source file or directory:

```bash
java -jar thirdparty/plantuml/plantuml.jar -tsvg path/to/diagram.puml
java -jar thirdparty/plantuml/plantuml.jar -tsvg path/to/diagrams
```

The downloaded JAR is intentionally ignored by Git. This document, the pinned
version, and the checksum are kept in the repository instead.
