<template>
  <h1 :class="$tt('headline3')">Create New Customer</h1>
  <ui-form nowrap item-margin-bottom="16" label-width="80">
    <ui-card>
      <!-- Customer Section -->
      <ui-card class="customer">
        <ui-card-text><h2 :class="[$tt('headline4')]">Customer {{ customer.company_name }} {{ customer.first_name }}
          {{ customer.last_name }}</h2>
        </ui-card-text>
        <ui-form-field>
          <ui-textfield required v-model="customer.first_name" helper-text-id="first-name-helper-text">First Name
          </ui-textfield>
          <ui-textfield-helper id="first-name-helper-text" v-model:validMsg="validMsg.first_name"></ui-textfield-helper>
          <ui-textfield required v-model="customer.last_name">Last Name</ui-textfield>
          <ui-textfield v-model="customer.company_name">Company Name</ui-textfield>
        </ui-form-field>
        <ui-card class="customer-contacts">
          <ui-card-text><h3 :class="$tt('headline5')">Customer Contact(s)</h3></ui-card-text>
          <ui-form-field>
            <ui-checkbox
                input-id="customer-contact-same-customer"
                v-model="customer.contact_same_as_customer">
            </ui-checkbox>
            <label for="customer-contact-same-customer">Same as Customer</label>
          </ui-form-field>
          <div class="contact" v-for="(contact, index) in customer.contacts" :key="index" :contact="contact">
            <ui-form-field>
              <ui-textfield v-if="!customer.contact_same_as_customer" v-model="contact.first_name"
              >First Name
              </ui-textfield>
              <ui-textfield v-else disabled>{{
                  customer.first_name ? customer.first_name : "First Name"
                }}
              </ui-textfield>
              <ui-textfield v-if="!customer.contact_same_as_customer" v-model="contact.last_name"
              >Last Name
              </ui-textfield>
              <ui-textfield v-else disabled>{{ customer.last_name ? customer.last_name : "Last Name" }}</ui-textfield>
              <ui-textfield v-model="contact.email" type="email">Email
                <template #after>
                  <ui-textfield-icon>email</ui-textfield-icon>
                </template>
              </ui-textfield>
              <ui-textfield v-model="contact.phone" type="tel" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
              >Phone
                <template #after>
                  <ui-textfield-icon>phone</ui-textfield-icon>
                </template>
              </ui-textfield>
            </ui-form-field>
          </div>
        </ui-card>
      </ui-card>

      <!-- Service Location Section -->
      <ui-card class="service-locations">
        <ui-card-text><h2 :class="$tt('headline4')">Service Location(s)</h2></ui-card-text>
        <ui-card v-for="(location, index) in customer.service_locations" :service_location="location"
                 :key="index" class="location">

          <ui-card-text><h3 :class="$tt('headline5')">Location {{
              location.name ? location.name : location.address_line_1
            }}</h3></ui-card-text>
          <ui-textfield v-model="location.name">Name</ui-textfield>
          <ui-textfield v-model="location.address_line_1">Street Address</ui-textfield>
          <ui-textfield v-model="location.address_line_2">Apt, Ste, etc...</ui-textfield>

          <ui-card>
            <ui-card-text>
              <h4 :class="$tt('headline6')">Contact(s)
                <ui-form-field>
                  <ui-checkbox :input-id="`service-contact-same-as-customer-contact-${index}`"
                               v-model="location.contact_same_as_customer"
                               type="checkbox"></ui-checkbox>
                  <label :for="`service-contact-same-as-customer-contact-${index}`">Same as Customer Contact</label>
                </ui-form-field>
              </h4>
            </ui-card-text>
            <ui-form-field v-if="!location.contact_same_as_customer">
              <div class="contact" v-for="(contact, index) in location.contacts" :key="index" :contact="contact">
                <ui-textfield v-model="contact.first_name">First Name</ui-textfield>
                <ui-textfield v-model="contact.last_name">Last Name</ui-textfield>
                <ui-textfield v-model="contact.email" type="email">Email
                  <template #after>
                    <ui-textfield-icon>email</ui-textfield-icon>
                  </template>
                </ui-textfield>
                <ui-textfield v-model="location.contacts.phone" type="tel"
                >Phone
                  <template #after>
                    <ui-textfield-icon>phone</ui-textfield-icon>
                  </template>
                </ui-textfield>
              </div>
            </ui-form-field>
          </ui-card>
        </ui-card>
      </ui-card>

      <ui-card class="billing-locations">
        <ui-card-text>
          <h2 :class="$tt('headline4')">Billing Location
            <ui-form-field>
              <ui-checkbox input-id="same-as-service-address"
                           v-model="customer.billing_location.location_same_as_service_location"
                           type="checkbox"></ui-checkbox>
              <label for="same-as-service-address">Same as Service Location</label>
            </ui-form-field>
          </h2>
        </ui-card-text>
        <ui-form-field class="location" v-if="!customer.billing_location.location_same_as_service_location">
          <ui-textfield id="billing-address-line-1" v-model="customer.billing_location.address_line_1"
                        placeholder="Address"></ui-textfield>
          <ui-textfield id="billing-address-line-2" v-model="customer.billing_location.address_line_2"
                        placeholder="Apt, Suite, etc.."></ui-textfield>
        </ui-form-field>
        <ui-card>
          <ui-card-text>
            <h3 :class="$tt('headline5')">Contact(s)
              <ui-form-field>
                <ui-checkbox :input-id="`billing-contact-same-as-customer-contact`"
                             v-model="customer.billing_location.contact_same_as_customer"
                             type="checkbox"></ui-checkbox>
                <label :for="`billing-contact-same-as-customer-contact`">Same as Customer</label>
              </ui-form-field>
            </h3>
          </ui-card-text>
          <div v-if="!customer.billing_location.contact_same_as_customer"
               class="service-address-contact">
            <div v-for="(contact, index) in customer.billing_location.contacts" :key="index" :contact="contact">
              <ui-textfield v-model="customer.billing_location.contacts.first_name">First Name</ui-textfield>
              <ui-textfield v-model="customer.billing_location.contacts.last_name">Last Name</ui-textfield>
              <ui-textfield v-model="customer.billing_location.contacts.email">Email
                <template #after>
                  <ui-textfield-icon>email</ui-textfield-icon>
                </template>
              </ui-textfield>
              <ui-textfield v-model="customer.billing_location.contacts.phone" type="tel">Phone
                <template #after>
                  <ui-textfield-icon>phone</ui-textfield-icon>
                </template>
              </ui-textfield>
            </div>
          </div>
        </ui-card>
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
  first_name: {
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
        first_name: "",
        last_name: "",
        company_name: "",
        contact_same_as_customer: true,
        contacts: [],
        service_locations: [],
      },
      message: "",
      valid: false
    }
  },
  created() {
    this.customer.service_locations.push(this.addLocation())
    this.customer.billing_location = this.addLocation()
    this.customer.billing_location.location_same_as_service_location = true
    this.customer.contacts.push(this.addContact())
  },
  methods: {
    submit() {
      let result = this.validator.validate(this.customer)

      let {valid, validMsg} = result;
      this.validMsg = validMsg;

      if (valid) {
        this.$toast('ok');
        console.log(this.customer)
      }
    },
    addContact() {
      return {first_name: "", last_name: "", emails: [{email: ''}], phones: [{phone: ""}]}
    },
    addLocation() {
      return {
        name: "",
        address_line_1: "",
        address_line_2: "",
        latitude: "",
        longitude: "",
        contact_same_as_customer: true,
        contacts: [this.addContact()],
      }
    }
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