# Integration Test Plan

Integration testing in ACA-Py consists of 3 different levels or types.
1. Interop profile (AATH) BDD tests. 
2. ACA-Py specific BDD tests.
3. End to End tests.

### Interop profile (AATH) BDD tests

Interoperability is extremely important in the aries community. When implementing or changing features that are included in the [aries interop profile](https://github.com/hyperledger/aries-rfcs/blob/main/concepts/0302-aries-interop-profile/README.md) the developer should try to add tests to this test suite. The tests will then be ran for PR's and scheduled workflows for acapy <--> acapy agents.

These tests are contained in a separate repo [AATH](https://github.com/hyperledger/aries-agent-test-harness). They use the behave syntax and a http back channel. 


### ACA-Py specific BDD tests

These tests leverage the demo agent and also use behave syntax and a back channel. See [README](./BDDTests.md)

These tests should be used to test RFCS protocols that are specific to aca-py and not in the interop profile. They can also be used for specific features from a fresh environment.

### End to End tests

These tests utilize the minimal example [agent](https://github.com/Indicio-tech/acapy-minimal-example) produced by Indicio.  


