# Integration Test Plan

Integration testing in ACA-Py consists of 3 different levels or types.
1. Interop profile (AATH) BDD tests. 
2. ACA-Py specific BDD tests.
3. End to End tests.

## Interop profile (AATH) BDD tests

Interoperability is extremely important in the aries community. When implementing or changing features that are included in the [aries interop profile](https://github.com/hyperledger/aries-rfcs/blob/main/concepts/0302-aries-interop-profile/README.md) the developer should try to add tests to this test suite. The tests will then be ran for PR's and scheduled workflows for acapy <--> acapy agents.

These tests are contained in a separate repo [AATH](https://github.com/hyperledger/aries-agent-test-harness). They use the gherkin syntax and a http back channel. 


## ACA-Py specific BDD tests

These tests leverage the demo agent and also use behave syntax and a back channel. See [README](./BDDTests.md)

These tests are another tool for leveraging the demo agent and the gherkin syntax. They should not be used to test features that involve the interop profile, as they can not be used to test against other frameworks. None of the tests that are covered by the AATH tests will be ran automatically. They are here because some developers may prefer the testing strategy and can be useful for explicit testing steps and protocols not included in the interop profile.  

## Scenario testing

These tests utilize the minimal example [agent](https://github.com/Indicio-tech/acapy-minimal-example) produced by Indicio. They exist in the `integration-tests` directory. They are very useful for running specific test plans and checking webhooks.

