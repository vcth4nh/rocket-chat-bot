import React, { useState } from 'react';
import FormInput from '../components/FormInput';
import OptionCheckbox from '../components/OptionCheckbox';
import { createPolicy, deletePolicy } from '../services/policyService'; // Import services

const HomePage = () => {
  const [blacklist, setBlacklist] = useState([]);
  const [regexList, setRegexList] = useState([]);
  const [wordLimit, setWordLimit] = useState(0);
  const [detectSecrets, setDetectSecrets] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Add a word to the blacklist tags and call the createPolicy API
  const handleBlacklistInput = async (e) => {
    if (e.key === 'Enter' && e.target.value.trim() !== '') {
      e.preventDefault();
      const newWord = e.target.value.trim();

      try {
        const createdPolicy = await createPolicy({
          type: 'blacklist',
          value: newWord,
        });
        setBlacklist([...blacklist, { id: createdPolicy.id, value: newWord }]);
        setSuccessMessage(`Blacklist word "${newWord}" added successfully!`);
        e.target.value = '';
      } catch (err) {
        setError('Failed to add blacklist word.');
        console.error(err);
      }
    }
  };

  // Add a regex to the regexList tags and call the createPolicy API
  const handleRegexInput = async (e) => {
    if (e.key === 'Enter' && e.target.value.trim() !== '') {
      e.preventDefault();
      const newRegex = e.target.value.trim();

      try {
        const createdPolicy = await createPolicy({
          type: 'regex',
          value: newRegex,
        });
        setRegexList([...regexList, { id: createdPolicy.id, value: newRegex }]);
        setSuccessMessage(`Regex "${newRegex}" added successfully!`);
        e.target.value = '';
      } catch (err) {
        setError('Failed to add regex.');
        console.error(err);
      }
    }
  };

  // Call the createPolicy API for word limit when form is submitted
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createPolicy({
        type: 'wordLimit',
        value: wordLimit.toString(),
      });

      setSuccessMessage('Word limit policy created successfully!');
      setError('');
    } catch (err) {
      setError('Failed to create word limit policy.');
      console.error(err);
    }
  };

  // Remove a tag from the blacklist and call the deletePolicy API
  const removeBlacklistTag = async (index) => {
    const tag = blacklist[index];
    try {
      await deletePolicy(tag.id); // Call delete API
      setBlacklist(blacklist.filter((_, i) => i !== index));
      setSuccessMessage(`Blacklist word "${tag.value}" removed successfully!`);
    } catch (err) {
      setError('Failed to remove blacklist word.');
      console.error(err);
    }
  };

  // Remove a tag from the regexList and call the deletePolicy API
  const removeRegexTag = async (index) => {
    const tag = regexList[index];
    try {
      await deletePolicy(tag.id); // Call delete API
      setRegexList(regexList.filter((_, i) => i !== index));
      setSuccessMessage(`Regex "${tag.value}" removed successfully!`);
    } catch (err) {
      setError('Failed to remove regex.');
      console.error(err);
    }
  };

  return (
    <div className="home-page">
      <h2>Web Portal Settings</h2>
      {error && <p className="error-message">{error}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>}

      <form onSubmit={handleSubmit}>
        {/* Blacklist Words */}
        <div className="form-group">
          <label htmlFor="blacklist">Blacklist Words (Press Enter to Add):</label>
          <input
            id="blacklist"
            type="text"
            onKeyDown={handleBlacklistInput}
            placeholder="Type a word and press Enter"
          />
          <div className="tags-container">
            {blacklist.map((tag, index) => (
              <div key={tag.id} className="tag">
                {tag.value}
                <button
                  type="button"
                  className="remove-tag"
                  onClick={() => removeBlacklistTag(index)}
                >
                  &times;
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Custom Regex */}
        <div className="form-group">
          <label htmlFor="regex">Custom Regex (Press Enter to Add):</label>
          <input
            id="regex"
            type="text"
            onKeyDown={handleRegexInput}
            placeholder="Type a regex and press Enter"
          />
          <div className="tags-container">
            {regexList.map((regex, index) => (
              <div key={regex.id} className="tag">
                {regex.value}
                <button
                  type="button"
                  className="remove-tag"
                  onClick={() => removeRegexTag(index)}
                >
                  &times;
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Word Limit */}
        <FormInput
          id="word-limit"
          label="Word Count Limit:"
          type="number"
          value={wordLimit}
          onChange={(e) => setWordLimit(Number(e.target.value))}
          placeholder="Enter a maximum word count"
        />

        {/* Detect Secrets */}
        <OptionCheckbox
          id="detect-secrets"
          label="Detect Secrets (default enabled)"
          checked={detectSecrets}
          onChange={(e) => setDetectSecrets(e.target.checked)}
        />

        {/* Submit */}
        <button type="submit">Submit Word Limit</button>
      </form>
    </div>
  );
};

export default HomePage;
