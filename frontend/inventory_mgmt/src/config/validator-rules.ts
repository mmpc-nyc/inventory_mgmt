import { helpers } from 'balm-ui'; // Default Usage
// OR
// import helpers from 'balm-ui/utils/helpers'; // ### Individual Usage

export default {
  required: {
    validate(value: string) {
      return !helpers.isEmpty(value);
    },
    message: '%s is required'
  },
  phone_number: {
    validate(value: string) {
      return /\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/.test(value);
    },
    message: 'Invalid phone number'
  },
  password: {
    validate(value: string) {
      return /^\w+$/.test(value);
    },
    message: '%s must be a letter, digit or underline'
  }
};