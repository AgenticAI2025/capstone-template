# 🛡️ AI-Powered AML Detection System - Capstone Project Instructions

## 📋 Project Overview

Welcome to the **AI-Powered Anti-Money Laundering (AML) Detection System** capstone project! This comprehensive project will guide you through building a sophisticated AML detection system using modern AI technologies including LangGraph, OpenAI, and Langfuse.

### 🎯 Learning Objectives
By the end of this project, you will have:
- Built a complete AML detection workflow using LangGraph
- Integrated OpenAI models for risk assessment
- Implemented observability with Langfuse
- Created evaluation frameworks for AI systems
- Generated automated SAR (Suspicious Activity Report) drafts

---

## 📊 Project Structure & Phases

The project is divided into **6 phases**, each building upon the previous one:

| Phase | Focus Area | Duration | Marks | Key Deliverables |
|-------|------------|----------|-------|------------------|
| **Phase 1** | Setup & Orientation | ~1 hour | 10 | Environment setup, API keys, connectivity |
| **Phase 2** | Graph & State Design | ~1.5 hours | 15 | AMLState definition, graph structure |
| **Phase 3** | Risk Logic Implementation | ~2 hours | 20 | LLM-powered risk analysis nodes |
| **Phase 4** | Dynamic Routing & Decision Logic | ~1.5 hours | 15 | Risk aggregation, conditional routing |
| **Phase 5** | Langfuse Integration | ~2 hours | 15 | Observability and experiment tracking |
| **Phase 6** | Evaluation & Scoring | ~2 hours | 15 | Performance evaluation and metrics |
| **Phase 7** | Reporting & Dashboard | ~1.5 hours | 10 | SAR generation, typology classification |

**Total Marks: 100**

---

## 🚀 Phase 1: Setup & Orientation (10 Marks)

### 📝 Tasks & Learning Outcomes
- Install required dependencies (LangGraph, OpenAI, Langfuse)
- Configure API keys securely
- Verify connectivity with all services
- Understand the project structure

### 🎯 Deliverables (10 Marks)
| Task | Marks | Description |
|------|-------|-------------|
| Successful installation | 2 | All dependencies installed without errors |
| API key setup | 3 | Environment variables configured correctly |
| OpenAI connectivity | 2 | Test call to OpenAI API successful |
| Langfuse connectivity | 2 | Trace creation and verification successful |
| Langfuse playground testing | 1 | Test prompts in Langfuse playground |

### 💡 Hints & Tips
- **API Keys**: Store your keys in a `.env` file, never commit them to version control
- **Dependencies**: Use `%pip install` in Jupyter for better package management
- **Troubleshooting**: If you get import errors, restart your kernel after installing packages
- **Environment**: Make sure you're using Python 3.8+ for compatibility

### 🔧 Common Issues & Solutions
- **ImportError**: Restart kernel after installing packages
- **API Key Error**: Check your `.env` file format and key names
- **Connection Timeout**: Verify your internet connection and API key validity

---

## 🧪 Prompt Engineering & Langfuse Playground Testing

### 📝 Sample Prompts for Testing

Before implementing the full system, test your prompts in the **Langfuse Playground** to ensure they produce consistent, high-quality outputs. Here are sample prompts for each risk analysis node:

#### 🔍 Document Analysis Prompt
```
You are an AML risk analyst. Given a transaction, customer, and attached document snippets, assess *document-related* AML risk.
Consider:
- Trade-based laundering indicators (over/under-invoicing, quantity/price mismatches)
- Falsified or unverifiable invoices/permits
- Inconsistent counterparties, HS codes, or commodity categories
- Sanctions/PEP hints in documents
- Timing anomalies vs. shipment/payment terms

Output STRICT JSON with:
- "score": integer 0–100 (higher = higher risk, based only on documents)
- "rationale": concise explanation (<120 words), citing specific inconsistencies

TRANSACTION:
{
  "amount": 200000,
  "origin_country": "IR",
  "destination_country": "DE",
  "parties": ["tehran_exporters"],
  "timestamp": "2025-03-27T19:20:16.639571",
  "documents": ["Trade Agreement #IR-789"]
}

CUSTOMER:
{
  "name": "Ali Reza",
  "account_age_days": 45,
  "transaction_history": []
}

DOCUMENTS:
["Trade Agreement #IR-789"]

Respond in JSON only.
```

#### 🌍 Geographic Risk Prompt
```
You are an AML analyst specializing in geographic risk assessment.
Evaluate the given transaction for cross-border risk based on:
- Origin, destination, and intermediate countries
- Presence of high-risk jurisdictions (FATF grey / black list)
- Tax havens or offshore financial centres
- Sanctioned regions or entities commonly involved in evasion
- Unusual routing patterns (3+ intermediaries or circular routes)

Output STRICT JSON with:
{
  "score": integer 0–100,
  "rationale": "<short explanation < 100 words>"
}

TRANSACTION:
{
  "amount": 200000,
  "origin_country": "IR",
  "destination_country": "DE",
  "parties": ["tehran_exporters"],
  "timestamp": "2025-03-27T19:20:16.639571",
  "documents": ["Trade Agreement #IR-789"]
}

Respond in JSON only.
```

#### 👤 Behavioral Risk Prompt
```
You are an AML analyst evaluating transactional behavior patterns.
Given a customer's transaction history and current transaction, assess behavioral risk based on:

- Frequency of similar transactions (possible structuring)
- Sudden spikes in volume or velocity
- Account age vs transaction size
- Unusual transaction times or counterparties
- Round-number or repeated sub-threshold transactions

Return STRICT JSON with:
{
  "score": integer 0–100,
  "rationale": "<concise explanation (<120 words)>"
}

TRANSACTION:
{
  "amount": 9500,
  "origin_country": "US",
  "destination_country": "CA",
  "parties": ["retail_chain_inc"],
  "timestamp": "2025-03-27T19:20:16.639571",
  "documents": ["Invoice #SMF-4587"],
  "frequency": 8
}

CUSTOMER:
{
  "name": "James Smith",
  "account_age_days": 120,
  "transaction_history": [
    {
      "amount": 9200,
      "timestamp": "2025-03-27T17:20:16.639571"
    },
    {
      "amount": 9350,
      "timestamp": "2025-03-27T15:20:16.639571"
    }
  ]
}

HISTORY:
[
  {
    "amount": 9200,
    "timestamp": "2025-03-27T17:20:16.639571"
  },
  {
    "amount": 9350,
    "timestamp": "2025-03-27T15:20:16.639571"
  }
]

Respond in JSON only.
```

#### 🪙 Crypto Risk Prompt
```
You are an AML analyst specializing in crypto asset transactions.
Assess the transaction below for crypto-related money laundering risk.

Consider:
- Wallet age (new or short-lived)
- Use of mixers, privacy coins, or tumblers
- Cross-chain swaps (multiple assets or obfuscation attempts)
- Unusually large or fragmented transfers
- Known typologies (layering, conversion through DeFi bridges)

Output STRICT JSON with:
{
  "score": integer 0–100,
  "rationale": "<concise reasoning (<120 words)>"
}

TRANSACTION:
{
  "amount": 50000,
  "asset_type": "CRYPTO",
  "crypto_type": "Bitcoin",
  "wallet_age_days": 5,
  "mixer_used": true,
  "cross_chain_swaps": 3
}

CUSTOMER:
{
  "name": "Anonymous User",
  "account_age_days": 2,
  "transaction_history": []
}

Respond in JSON only.
```

### 🎮 Langfuse Playground Testing Steps

1. **Access Langfuse Playground**
   - Go to [Langfuse Playground](https://cloud.langfuse.com/playground)
   - Sign in with your Langfuse credentials

2. **Test Each Prompt**
   - Copy each sample prompt above
   - Paste into the playground
   - Run multiple iterations to test consistency
   - Verify JSON output format

3. **Evaluate Results**
   - Check for consistent JSON structure
   - Verify score ranges (0-100)
   - Assess rationale quality and relevance
   - Note any parsing errors or inconsistencies

4. **Iterate and Improve**
   - Modify prompts based on results
   - Test edge cases and unusual inputs
   - Document successful prompt patterns
   - Save working prompts for implementation

### 📚 Langfuse Documentation References

- **Getting Started**: [Langfuse Quickstart Guide](https://langfuse.com/docs/get-started)
- **Playground Usage**: [Playground Documentation](https://langfuse.com/docs/playground)
- **Prompt Engineering**: [Best Practices](https://langfuse.com/docs/prompts)
- **Tracing**: [Trace Management](https://langfuse.com/docs/tracing)
- **Evaluation**: [Evaluation Framework](https://langfuse.com/docs/evaluation)

### 💡 Playground Testing Tips

- **Consistency**: Run each prompt 3-5 times to check for consistent outputs
- **Edge Cases**: Test with unusual or extreme input values
- **JSON Validation**: Ensure all responses are valid JSON
- **Score Ranges**: Verify scores stay within 0-100 range
- **Rationale Quality**: Check that explanations are relevant and concise

---

## 🏗️ Phase 2: Graph & State Design (15 Marks)

### 📝 Tasks & Learning Outcomes
- Define the `AMLState` TypedDict structure
- Create utility functions for state management
- Build the initial graph scaffold with placeholder nodes
- Test the graph execution flow
- Visualize the graph structure

### 🎯 Deliverables (15 Marks)
| Task | Marks | Description |
|------|-------|-------------|
| AMLState definition + utilities | 5 | Complete state structure with helper functions |
| Graph nodes scaffolded | 5 | All nodes defined with proper connections |
| Test run and visualization | 5 | Successful execution and graph visualization |

### 💡 Hints & Tips
- **State Design**: Keep your state structure simple but comprehensive
- **Node Naming**: Use descriptive names for your nodes (e.g., "Document Analysis", "Geographic Risk")
- **Graph Visualization**: Use `get_graph().draw_mermaid_png()` for visual debugging
- **Testing**: Start with simple test cases before complex scenarios

### 🔧 Common Issues & Solutions
- **State Errors**: Ensure all required fields have default values
- **Graph Compilation**: Check that all nodes are properly connected
- **Visualization Issues**: Install `pyppeteer` if graph rendering fails

---

## 🤖 Phase 3: Risk Logic Implementation (20 Marks)

### 📝 Tasks & Learning Outcomes
- Implement OpenAI-powered Document Analysis node
- Create Geographic Risk assessment node
- Build Behavioral Risk analysis node
- Develop Crypto Risk evaluation node
- Integrate all nodes into the complete graph

### 🎯 Deliverables (20 Marks)
| Task | Marks | Description |
|------|-------|-------------|
| Document Node with OpenAI | 5 | LLM-powered document risk analysis |
| Geographic Node with OpenAI | 5 | Country and routing risk assessment |
| Behavioral Node with OpenAI | 5 | Transaction pattern analysis |
| Crypto Node with OpenAI | 5 | Cryptocurrency-specific risk evaluation |

### 💡 Hints & Tips
- **Prompt Engineering**: Write clear, specific prompts for consistent outputs
- **JSON Parsing**: Always include error handling for LLM responses
- **Score Clamping**: Use the `clamp_score()` utility to ensure scores are 0-100
- **Rationale Quality**: Ask for concise but informative explanations

### 🔧 Common Issues & Solutions
- **JSON Parsing Errors**: Implement fallback parsing for malformed responses
- **Inconsistent Scores**: Use temperature=0.2 for more consistent outputs
- **Memory Issues**: Process one node at a time for large datasets

---

## ⚙️ Phase 4: Dynamic Routing & Decision Logic (15 Marks)

### 📝 Tasks & Learning Outcomes
- Implement risk score aggregation algorithms
- Create conditional routing logic
- Build decision engine for SAR triggering
- Test the complete workflow with sample data

### 🎯 Deliverables (15 Marks)
| Task | Marks | Description |
|------|-------|-------------|
| Risk aggregation & routing functions | 5 | Weighted scoring and conditional logic |
| Decision Engine node integration | 5 | SAR triggering and risk classification |
| Full dynamic test run | 5 | Successful execution with sample_cases.json |

### 💡 Hints & Tips
- **Weighted Scoring**: Use different weights for different risk types
- **Threshold Tuning**: Start with conservative thresholds (e.g., 80 for SAR)
- **Routing Logic**: Keep routing decisions simple and deterministic
- **Testing**: Use the provided sample_cases.json for comprehensive testing

### 🔧 Common Issues & Solutions
- **Score Aggregation**: Ensure all scores are properly weighted
- **Routing Errors**: Test each routing path independently
- **Performance**: Consider caching for repeated calculations

---

## 📊 Phase 5: Langfuse Integration (15 Marks)

### 📝 Tasks & Learning Outcomes
- Initialize Langfuse client
- Instrument LLM calls with tracing
- Log batch results to Langfuse
- Create comprehensive observability

### 🎯 Deliverables (15 Marks)
| Task | Marks | Description |
|------|-------|-------------|
| Langfuse client & tracing wrapper | 5 | Proper client initialization and tracing setup |
| LLM analysis functions instrumented | 5 | All nodes properly traced |
| Batch results logged to Langfuse | 5 | Trace creation and metadata logging |

### 💡 Hints & Tips
- **Tracing**: Use consistent naming conventions for traces
- **Metadata**: Include relevant context in trace metadata
- **Error Handling**: Wrap tracing calls in try-catch blocks
- **Flushing**: Always call `langfuse.flush()` to ensure data is sent

### 🔧 Common Issues & Solutions
- **Trace Loss**: Ensure proper flushing of traces
- **Connection Errors**: Check Langfuse credentials and network connectivity
- **Performance**: Batch operations when possible

---

## 📈 Phase 6: Evaluation & Scoring (15 Marks)

### 📝 Tasks & Learning Outcomes
- Design evaluation rubrics for AML reasoning
- Implement automated scoring metrics
- Generate performance summaries
- Log evaluation results to Langfuse dashboard

### 🎯 Deliverables (15 Marks)
| Task | Marks | Description |
|------|-------|-------------|
| Evaluation rubric & metrics | 5 | Risk alignment, faithfulness, alert accuracy |
| Scenarios evaluated & summary | 5 | All test cases evaluated with metrics |
| Metrics logged to Langfuse | 5 | Results stored in Langfuse with metadata |

### 💡 Hints & Tips
- **Evaluation Metrics**: Focus on practical AML-relevant measures
- **Baseline Comparison**: Compare against expected outcomes
- **Statistical Analysis**: Calculate averages and distributions
- **Documentation**: Document your evaluation methodology

### 🔧 Common Issues & Solutions
- **Metric Calculation**: Ensure all metrics are properly normalized
- **Data Consistency**: Validate evaluation results before logging
- **Performance**: Use vectorized operations for large datasets

---

## 📋 Phase 7: Reporting & Dashboard (10 Marks)

### 📝 Tasks & Learning Outcomes
- Generate consolidated reports (CSV, charts)
- Create automated SAR drafts
- Classify threat typologies
- Build Streamlit dashboard

### 🎯 Deliverables (10 Marks)
| Task | Marks | Description |
|------|-------|-------------|
| Consolidated report generation | 3 | CSV export and visualization |
| SAR draft generation | 3 | Automated SAR creation for high-risk cases |
| Typology classification | 2 | Threat stage classification |
| Dashboard scaffold | 2 | Basic Streamlit interface |

### 💡 Hints & Tips
- **Report Format**: Use clear, professional formatting
- **SAR Quality**: Ensure SARs are audit-ready and factual
- **Typology Accuracy**: Use clear classification criteria
- **Dashboard UX**: Focus on key metrics and filtering

### 🔧 Common Issues & Solutions
- **PDF Generation**: Install reportlab for PDF creation
- **File Paths**: Use absolute paths for file operations
- **Dashboard Errors**: Test Streamlit app locally first

---

## 🎯 Marking Criteria & Evaluation

### 📊 Overall Assessment Framework

| Category | Weight | Description |
|----------|--------|-------------|
| **Technical Implementation** | 40% | Code quality, architecture, best practices |
| **Functionality** | 30% | Working features, error handling, edge cases |
| **Documentation** | 15% | Code comments, README, explanations |
| **Innovation** | 10% | Creative solutions, optimizations, extensions |
| **Presentation** | 5% | Final demo, code organization, deliverables |

### 🏆 Grade Boundaries

| Grade | Marks | Description |
|-------|-------|-------------|
| **A+** | 90-100 | Exceptional work with innovative solutions |
| **A** | 80-89 | Excellent implementation with minor issues |
| **B+** | 70-79 | Good work with some areas for improvement |
| **B** | 60-69 | Satisfactory completion of requirements |
| **C** | 50-59 | Basic requirements met with significant issues |
| **F** | 0-49 | Incomplete or non-functional submission |

### 📝 Detailed Evaluation Criteria

#### Technical Implementation (40 marks)
- **Code Quality**: Clean, readable, well-structured code
- **Architecture**: Proper separation of concerns, modular design
- **Error Handling**: Robust error handling and edge case management
- **Performance**: Efficient algorithms and resource usage
- **Best Practices**: Following Python and ML best practices

#### Functionality (30 marks)
- **Core Features**: All required features implemented and working
- **Integration**: Proper integration between components
- **Testing**: Comprehensive testing with sample data
- **Edge Cases**: Handling of unusual inputs and scenarios
- **User Experience**: Intuitive and user-friendly interface

#### Documentation (15 marks)
- **Code Comments**: Clear, helpful comments throughout code
- **README**: Comprehensive project documentation
- **Explanations**: Clear explanations of complex logic
- **Setup Instructions**: Easy-to-follow setup and installation guide
- **Troubleshooting**: Common issues and solutions documented

#### Innovation (10 marks)
- **Creative Solutions**: Novel approaches to problems
- **Optimizations**: Performance or accuracy improvements
- **Extensions**: Additional features beyond requirements
- **Research**: Evidence of research and experimentation
- **Originality**: Unique contributions to the project

#### Presentation (5 marks)
- **Code Organization**: Logical file structure and naming
- **Deliverables**: All required deliverables present and complete
- **Final Demo**: Clear demonstration of working system
- **Professionalism**: Professional presentation and communication

---

## 🚨 Common Pitfalls & How to Avoid Them

### ⚠️ Technical Pitfalls
1. **API Key Exposure**: Never commit API keys to version control
2. **Memory Issues**: Process data in batches for large datasets
3. **JSON Parsing**: Always handle malformed LLM responses
4. **Dependency Conflicts**: Use virtual environments
5. **Async Issues**: Handle async operations properly

### ⚠️ Project Management Pitfalls
1. **Scope Creep**: Focus on core requirements first
2. **Testing Neglect**: Test early and often
3. **Documentation Delay**: Document as you code
4. **Version Control**: Commit frequently with clear messages
5. **Time Management**: Allocate time properly across phases

### ⚠️ Evaluation Pitfalls
1. **Incomplete Implementation**: Ensure all phases are complete
2. **Poor Error Handling**: Handle edge cases gracefully
3. **Lack of Testing**: Test with various input scenarios
4. **Missing Documentation**: Document your approach and decisions
5. **No Innovation**: Look for opportunities to improve and extend

---

## 🛠️ Development Environment Setup

### 📋 Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- Git for version control
- Text editor (VS Code recommended)

### 🔧 Required API Keys
- **OpenAI API Key**: For GPT model access
- **Langfuse Keys**: Public and Secret keys for observability

### 📦 Installation Commands
```bash
# Create virtual environment
python -m venv aml_env
source aml_env/bin/activate  # On Windows: aml_env\Scripts\activate

# Install dependencies
pip install langgraph langchain-openai langfuse python-dotenv
pip install pyppeteer reportlab streamlit pandas matplotlib

# Create .env file
touch .env
```

### 🔑 Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## 📚 Additional Resources

### 📖 Documentation Links
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Langfuse Documentation](https://langfuse.com/docs)
- [LangSmith Documentation](https://docs.smith.langchain.com/)

### 🎓 Learning Resources
- [AML Typologies Guide](https://www.fatf-gafi.org/publications/methodsandtrends/)
- [Risk Assessment Best Practices](https://www.bis.org/publ/bcbs239.htm)
- [Python Best Practices](https://docs.python-guide.org/)
- [Machine Learning Ethics](https://www.partnershiponai.org/)

### 🆘 Getting Help
- **Instructor Office Hours**: [Schedule through email]
- **Technical Support**: [Use DC Support email]
- **Peer Collaboration**: [You can create internal groups]

---

## 🎉 Success Tips

### 💪 Best Practices
1. **Start Early**: Begin each phase as soon as possible
2. **Test Frequently**: Run tests after each major change
3. **Document Everything**: Keep detailed notes of your approach
4. **Ask Questions**: Don't hesitate to seek clarification
5. **Collaborate**: Work with peers when appropriate

### 🚀 Pro Tips
1. **Version Control**: Use Git to track your progress
2. **Backup Work**: Save your work frequently
3. **Experiment**: Try different approaches and compare results
4. **Optimize**: Look for opportunities to improve performance
5. **Extend**: Consider additional features beyond requirements

### 🏆 Final Checklist
- [ ] All phases completed successfully
- [ ] Code is clean and well-documented
- [ ] All tests pass
- [ ] Documentation is complete
- [ ] Deliverables are ready
- [ ] Final demo is prepared

---

**Good luck with your AML Detection System capstone project! 🚀**

*Remember: This project is designed to be challenging but rewarding. Take your time, ask questions, and don't hesitate to seek help when needed.*
