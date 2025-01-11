import React from 'react';
import PropTypes from 'prop-types';

const OptionCheckbox = ({ id, label, checked, onChange }) => (
  <div className="form-group">
    <input
      type="checkbox"
      id={id}
      checked={checked}
      onChange={onChange}
    />
    <label htmlFor={id}>{label}</label>
  </div>
);

OptionCheckbox.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  checked: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired,
};

export default OptionCheckbox;
