# tradingsys
<h2>Overview</h2>
Personal Trading System
<br>
<h2>Roadmap</h2>
<p>This is to show the phases and the process of creating our trading system, from obtaining data to performing the execution. The main goal is to undertand and learn what are the necessary components to build such systems and learn the needed technical knowledge i.e latency, architecture, signal generation etc. We would show the key components in the following table:</p>

<hr>

#### Data Integration
In a trading system, we would need some way of storing our market data to be used for research later on. We would be automating the process of acquiring these data points and also ensuring the quality of the data. This would be set in a different repository.

##### Task List
- [ ] Setup pipeline to obtain master security key on daily
    - [x] Setup S3 bucket
    - [x] Setup SQL Schema and Table
    - [x] Write scraper class for generic web scraping function
    - [x] Write main function to parse the data that we need
    - [ ] Unit testing for our tools
    - [ ] Setup Orchestration Workflow
    - [ ] Setup Lambda function
    - [ ] Monitor workflow run
- [ ] Setup pipeline to obtain and store EOD OHLC data
    - [ ] Setup SQL Schema and Table
    - [ ] Write scraper class to parse the data we need
    - [ ] Backfill data to N years
    - [ ] Unit testing for our tools
    - [ ] Setup Orchestration Workflow
    - [ ] Setup Lambda function
    - [ ] Monitor workflow run
- [ ] Setup QA and logging system for our market data system

##### Technical requirement
1. Python (Low Frequency)
2. Docker
3. AWS
    - AWS Cloudwatch
    - AWS Lambda
    - AWS S3
    - AWS RDS

<hr>

#### Miscellaneous
- [ ] Check for ways to automate our builds
- [ ] 