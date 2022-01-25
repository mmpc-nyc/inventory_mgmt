<template>
  <h1 :class="$tt('headline3')">Create New Customer</h1>
  <ui-form horizontal>
    <ui-card>
      <ui-card class="customer">
        <ui-card-text><h2 :class="[$tt('headline4')]">Customer {{ customer.companyName }} {{ customer.firstName }}
          {{ customer.lastName }}</h2>
        </ui-card-text>
        <ui-form-field>
          <ui-textfield required v-model="customer.firstName" helper-text-id="first-name-helper-text">First Name
          </ui-textfield>
          <ui-textfield-helper id="first-name-helper-text" v-model:validMsg="validMsg.firstName"></ui-textfield-helper>
          <ui-textfield required v-model="customer.lastName">Last Name</ui-textfield>
          <ui-textfield v-model="customer.companyName">Company Name</ui-textfield>
        </ui-form-field>

        <ui-card-text><h3 :class="$tt('headline5')">Customer Contact</h3></ui-card-text>
        <ui-form-field class="contact">
          <ui-form-field>
            <ui-checkbox
                input-id="same-as-customer-name"
                v-model="customerContactSameAsCustomer">
            </ui-checkbox>
            <label for="same-as-customer-name">Same as Customer</label>
          </ui-form-field>
          <ui-form-field>
            <ui-textfield v-if="!customerContactSameAsCustomer" v-model="customer.contact.firstName"
            >First Name
            </ui-textfield>
            <ui-textfield v-else disabled>{{ customer.firstName ? customer.firstName : "First Name" }}</ui-textfield>
            <ui-textfield v-if="!customerContactSameAsCustomer" v-model="customer.contact.lastName"
            >Last Name
            </ui-textfield>
            <ui-textfield v-else disabled>{{ customer.lastName ? customer.lastName : "Last Name" }}</ui-textfield>
            <ui-textfield v-model="customer.contact.email" type="email">Email
              <template #after>
                <ui-textfield-icon>email</ui-textfield-icon>
              </template>
            </ui-textfield>
            <ui-textfield v-model="customer.contact.phone" type="tel" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
            >Phone
              <template #after>
                <ui-textfield-icon>phone</ui-textfield-icon>
              </template>
            </ui-textfield>
          </ui-form-field>
        </ui-form-field>
      </ui-card>

      <ui-card class="service">
        <ui-card-text><h2 :class="$tt('headline4')">Service Address</h2></ui-card-text>
        <ui-form-field>
          <ui-textfield v-model="serviceAddress.lineOne">Street Address</ui-textfield>
          <ui-textfield v-model="serviceAddress.lineTwo">Apt, Ste, etc...</ui-textfield>
        </ui-form-field>
        <ui-card-text><h3 :class="$tt('headline5')">Service Contact</h3></ui-card-text>
        <ui-form-field>
          <ui-checkbox input-id="service-contact-same-as-customer-contact"
                       v-model="serviceAddressContactSameAsCustomerContact"
                       type="checkbox"></ui-checkbox>
          <label for="service-contact-same-as-customer-contact">Same as Customer Contact</label>
        </ui-form-field>
        <ui-form-field v-if="!serviceAddressContactSameAsCustomerContact" class="service-address-contact">
          <ui-textfield v-model="serviceAddress.contact.firstName">First Name</ui-textfield>
          <ui-textfield v-model="serviceAddress.contact.lastName">Last Name</ui-textfield>
          <ui-textfield v-model="serviceAddress.contact.email" type="email">Email
            <template #after>
              <ui-textfield-icon>email</ui-textfield-icon>
            </template>
          </ui-textfield>
          <ui-textfield v-model="serviceAddress.contact.phone" type="tel"
          >Phone
            <template #after>
              <ui-textfield-icon>phone</ui-textfield-icon>
            </template>
          </ui-textfield>
        </ui-form-field>
      </ui-card>

      <ui-card class="billing">
        <ui-card-text><h2 :class="$tt('headline4')">Billing Address</h2></ui-card-text>
        <ui-form-field>
          <ui-checkbox input-id="same-as-service-address" v-model="billingAddressSameAsServiceAddress"
                       type="checkbox"></ui-checkbox>
          <label for="same-as-service-address">Same as Service Address</label>
        </ui-form-field>
        <ui-form-field class="billing-address" v-if="!billingAddressSameAsServiceAddress">
          <ui-textfield id="billing-address-line-1" v-model="billingAddress.lineOne"
                        placeholder="Address"></ui-textfield>
          <ui-textfield id="billing-address-line-2" v-model="billingAddress.lineTwo"
                        placeholder="Apt, Suite, etc.."></ui-textfield>
        </ui-form-field>
        <ui-card-text><h3 :class="$tt('headline5')">Billing Contact</h3></ui-card-text>
        <ui-form-field>
          <ui-checkbox :input-id="`billing-contact-same-as-customer-contact`"
                       v-model="billingAddressContactSameAsCustomerContact"
                       type="checkbox"></ui-checkbox>
          <label :for="`billing-contact-same-as-customer-contact`">Same as Customer</label>
        </ui-form-field>
        <ui-form-field v-if="!billingAddressContactSameAsCustomerContact" class="service-address-contact">
          <ui-textfield v-model="billingAddress.contact.firstName">First Name</ui-textfield>
          <ui-textfield v-model="billingAddress.contact.lastName">Last Name</ui-textfield>
          <ui-textfield v-model="billingAddress.contact.email">Email
            <template #after>
              <ui-textfield-icon>email</ui-textfield-icon>
            </template>
          </ui-textfield>
          <ui-textfield v-model="billingAddress.contact.phone" type="tel">Phone
            <template #after>
              <ui-textfield-icon>phone</ui-textfield-icon>
            </template>
          </ui-textfield>
        </ui-form-field>
      </ui-card>
      <ui-card-actions>
        <ui-button raised @click="submit">Submit</ui-button>
      </ui-card-actions>
    </ui-card>
  </ui-form>

</template>

<script>
import {useValidator} from "balm-ui";

const validations = {
  firstName: {
    label: 'First Name',
    validator: 'required',
  },
}
export default {
  name: "CustomerAdminCreate",
  data() {
    return {
      validMsg: {},
      validator: useValidator(),
      validations: validations,
      customer: {
        firstName: "",
        lastName: "",
        companyName: "",
        contact: {
          firstName: "",
          lastName: "",
          email: "",
          phone: "",
        },
      },
      serviceAddress: {
        lineOne: "",
        lineTwo: "",
        contact: {
          firstName: "",
          lastName: "",
          email: "",
          phone: "",
        },
      },
      billingAddress: {

        lineOne: "",
        lineTwo: "",
        contact: {
          firstName: "",
          lastName: "",
          email: "",
          phone: "",
        },
      },
      customerContactSameAsCustomer: true,
      serviceAddressContactSameAsCustomerContact: true,
      billingAddressSameAsServiceAddress: true,
      billingAddressContactSameAsCustomerContact: true,
      billingAddressContactSameAsServiceAddressContact: true,
      message: "",
      valid: false
    }
  },
  methods: {
    submit() {
      let result = this.validator.validate(this.customer)

      let {valid, validMsg} = result;
      this.validMsg = validMsg;

      if (valid) {
        this.$toast('ok');
      }
    },
  },
}
</script>

<style scoped lang="scss">
.mdc-card {
  margin: 1rem;
  padding-left: 1rem;
  padding-right: 1rem;
  padding-bottom: 1rem;
}

h2, h3, h4, h5 {
}
</style>