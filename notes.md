+## 1. Application level configuration
 +
 +```sh
 +fn apps config set myapp LOG_LEVEL debug
 +```
 +
 +## 2. Function configuration from func.yaml
 +
 +See [Function file](../function-file.md) for more info.
 +
 +## 3. Route level configuration
 +
 +```sh
 +fn routes config set myapp hello2 LOG_LEVEL info
 +```