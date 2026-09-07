FROM maven:3.9.9-eclipse-temurin-21@sha256:3a4ab3276a087bf276f79cae96b1af04f53731bec53fb2e651aca79e4b10211e AS java

FROM python:3.12.11-slim-bookworm@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7

COPY --from=java /opt/java/openjdk /opt/java/openjdk
COPY --from=java /usr/share/maven /usr/share/maven

ENV JAVA_HOME=/opt/java/openjdk \
    MAVEN_HOME=/usr/share/maven
ENV PATH="/opt/java/openjdk/bin:/usr/share/maven/bin:/opt/pmd/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        unzip \
        libstdc++6 \
    && curl -fL --retry 3 \
        https://github.com/pmd/pmd/releases/download/pmd_releases%2F7.17.0/pmd-dist-7.17.0-bin.zip \
        -o /tmp/pmd.zip \
    && unzip -q /tmp/pmd.zip -d /opt \
    && mv /opt/pmd-bin-7.17.0 /opt/pmd \
    && rm /tmp/pmd.zip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["python", "scripts/trial.py", "--help"]
