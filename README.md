# AI-enabled Semantic Search for National Classification of Occupation (NCO)

## 1. Track
Data Collection and Processing

---

## 2. Description

The National Classification of Occupation (NCO) is a standardized system for classifying occupations in India, aligned with the International Standard Classification of Occupations (ISCO). The current version, NCO-2015, includes detailed descriptions of 3,600 civilian occupations across 52 sectors, structured through an 8-digit hierarchical code.

**Current Challenges:**
- Requires exact keyword match
- Offers no semantic understanding of queries
- Demands extensive familiarity with the occupation taxonomy
- Is time-consuming, error-prone, and not scalable

**Example Problem:**  
To assign the occupation code for a "Sewing Machine Operator," a user must know its classification hierarchy across divisions and sub-groups without automation. This complexity can result in incorrect classification, leading to data quality issues that hinder policy planning and productivity. If unresolved, this challenge will continue to affect the efficiency and accuracy of official statistics, directly impacting national data systems and evidence-based governance.

---

## 3. Expected Outcomes/Solutions

Participants are expected to develop a prototype application that:

- Ingests and indexes NCO-2015 data
- Accepts free-text input from users (e.g., job title, description)
- Returns top N matching occupation codes with:
  - Semantic relevance ranking
  - Confidence scores
- Supports error handling and fallback suggestions
- Integration with voice input or multilingual support
- Admin panel to update or revise the occupation database
- Audit trails for search history or manual override

---

## 4. Relevance to National Priorities or Ongoing MoSPI Initiatives

This use case aligns with MoSPI's commitment to leveraging AI and frontier technologies for improving the quality, speed, and usability of official statistics. By enabling accurate, semantic, and intelligent occupation code assignment, it contributes to:

- High-quality, real-time data collection
- Efficient resource deployment in large-scale surveys
- Reduced manual errors and training overhead
- Modernization of classification systems

It directly strengthens MoSPI's capacity to deliver timely, high-quality, and policy-relevant official statistics.

**Improved Efficiency:** An AI/ML solution will reduce the cost and manual effort required for classifying the scanner data, if used in future.

**Enhanced Accuracy:** With automated classification and utilization of scanner data will more accurately capture the inflation or deflation which is critical for different policies in the country.

---

## 5. Background Resources or Datasets

MoSPI will provide:
- NCO-2015 data (PDF/Excel format)
  - Volume I: Mapping with NCO-2004
  - Volume II: Detailed job descriptions
- Sample queries and mapped codes (if available)

Participants may use pre-trained language models (e.g., BERT) and standard NLP resources, but final applications must operate within the context of Indian occupational taxonomies.

---

## 6. Key Features Required

### Data Ingestion & Processing
- Convert NCO datasets into structured formats (e.g., JSON, CSV)
- Normalize text for uniformity
- Preserve and represent hierarchy (4-digit groupings to 8-digit codes)

### Semantic Search Implementation
- Generate embeddings using NLP models (e.g., BERT, Sentence Transformers)
- Store indexed embeddings in a fast-retrieval system (e.g., FAISS)
- Return results with ranked relevance and confidence scores

### Synonym & Context Handling
- Map synonyms and variations (e.g., "tailor" vs. "sewing machine operator")
- Create a synonym/related term bank

### Query Interface
- Accept text/voice input
- Display top matches and allow user selection
- Include fallback and error messages

### Additional Features
- Support for multilingual input (Hindi and regional languages)
- Dashboards for usage statistics, performance, and audit trail
- API-based integration with MoSPI survey apps or portals

---

## 7. Impact Potential

The solution has high impact potential by:

- Reducing manual effort for enumerators and increasing accuracy
- Improving data consistency across regions and surveys
- Accelerating survey preparation and reducing training time
- Enabling scalable, intelligent systems for national classification tasks

---

## 8. Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-enabled-semantic-search-for-nco.git
   cd ai-enabled-semantic-search-for-nco
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate occupation embeddings:**
   ```bash
   python src/data_processing/create_occupation_embeddings.py
   ```

5. **Run the Streamlit application:**
   ```bash
   streamlit run src/streamlit_app.py
   ```

---

## 9. Usage

1. Open the Streamlit web interface in your browser
2. Enter a job description or occupation title in the search box
3. Click "Search NCO Codes" to get semantic matches
4. Review the top matching NCO codes with confidence scores
5. Select the most appropriate code for your use case

**Example Queries:**
- "Software developer who creates mobile apps"
- "Person who repairs electronic devices"
- "Teacher in primary school"
- "Mechanic for automobiles"

---

## 10. File Structure

```
ai-enabled-semantic-search-for-nco/
├── src/
│   ├── data_processing/
│   │   ├── create_occupation_embeddings.py
│   │   └── nco_data_processor.py
│   ├── models/
│   │   └── enhanced_search.py
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   │   └── nco_2015_data.csv
│   └── processed/
│       └── occupation_embeddings.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 11. Technologies Used

- **Python 3.9+**
- **Sentence Transformers** - For generating semantic embeddings
- **FAISS** - For fast similarity search
- **Streamlit** - For web interface
- **scikit-learn** - For additional ML utilities
- **pandas** - For data processing
- **numpy** - For numerical operations

---

## 12. Performance Metrics

The system achieves:
- **70%+ confidence scores** for accurate job classification
- **Sub-second response time** for semantic search queries
- **Support for 3,600+ occupation codes** from NCO-2015
- **Scalable architecture** for future enhancements

---

## 13. References

- [MoSPI Official Website](https://mospi.gov.in/)
- [e-Sankhyiki MoSPI](https://esankhyiki.mospi.gov.in/)
- [Data Innovation MoSPI](https://datainnovation.mospi.gov.in/)
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [FAISS Documentation](https://faiss.ai/)

---

## 14. Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

---

## 15. License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 16. Contact

For questions or support regarding this project, please create an issue in the GitHub repository or contact the development team.

---

**Note:** This project was developed as part of MoSPI's AI/ML initiative to modernize statistical data collection and processing systems in India.