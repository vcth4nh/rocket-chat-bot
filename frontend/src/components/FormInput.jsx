import React from 'react';
import PropTypes from 'prop-types';

const FormInput = ({ id, label, type, value, onChange, placeholder }) => (
  <div className="form-group">
    <label htmlFor={id}>{label}</label>
    <input
      type={type}
      id={id}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
  </div>
);

FormInput.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  type: PropTypes.string,
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  placeholder: PropTypes.string,
};

FormInput.defaultProps = {
  type: 'text',
  placeholder: '',
};

export default FormInput;
