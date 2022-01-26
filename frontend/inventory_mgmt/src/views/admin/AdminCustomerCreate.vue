<template>
  <h1 :class="$tt('headline3')">Create New Customer</h1>
  <ui-form type="|" item-margin-bottom="16" action-align="center">
    <template #default="{ actionClass }">
      <ui-card>
        <!-- Customer Section -->
        <ui-card class="customer">
          <ui-card-text><h2 :class="[$tt('headline4')]">Customer {{ customer.company_name }} {{ customer.first_name }}
            {{ customer.last_name }}</h2>
          </ui-card-text>
          <ui-form-field>
            <ui-textfield required v-model="customer.first_name" helper-text-id="first-name-helper-text">First Name
            </ui-textfield>
            <ui-textfield-helper id="first-name-helper-text"
                                 v-model:validMsg="validMsg.first_name"></ui-textfield-helper>
            <ui-textfield required v-model="customer.last_name">Last Name</ui-textfield>
            <ui-textfield v-model="customer.company_name">Company Name</ui-textfield>
            <ui-textfield v-model="customer.email" type="email">Email<template #after>
                    <ui-textfield-icon>phone</ui-textfield-icon>
                  </template></ui-textfield>
            <ui-textfield v-model="customer.phone" type="tel">Phone
              <template #after>
                <ui-textfield-icon>phone</ui-textfield-icon>
              </template>
            </ui-textfield>
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
                <ui-textfield v-model="contact.phone" type="tel"
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
          <div v-for="(location, index) in customer.service_locations" :service_location="location"
               :key="index" class="location">
            <div class="location-inputs">
              <google-map-auto-complete :class="`location-address-line-1`" :location="location"
                                        @setLocation="setLocation"></google-map-auto-complete>
              <ui-textfield :class="`location-address-line-2`" v-model="location.address_line_2">Apt, Ste, etc...
              </ui-textfield>
              <ui-textfield :class="`location-city`" v-model="location.city">City</ui-textfield>
              <ui-textfield :class="`location-state`" v-model="location.state">State</ui-textfield>
              <ui-textfield :class="`location-postal-code`" v-model="location.postal_code">Postal Code</ui-textfield>
            </div>
            <google-map :class="`location-map`" :location="location"></google-map>
            <ui-divider :class="`location-divider`">
              <ui-form-field>
                <ui-checkbox :input-id="`service-contact-same-as-customer-contact-${index}`"
                             v-model="location.contact_same_as_customer"
                             type="checkbox"></ui-checkbox>
                <label :for="`service-contact-same-as-customer-contact-${index}`">Same as Customer Contact</label>
              </ui-form-field>
            </ui-divider>
            <div :class="`location-contacts`" v-if="!location.contact_same_as_customer">
              <h3 :class="$tt('headline5')">Contact(s)</h3>
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
            </div>
          </div>
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
        <ui-form-field :class="actionClass">
          <ui-button raised @click="submit">Submit</ui-button>
        </ui-form-field>
      </ui-card>
    </template>
  </ui-form>

</template>

<script>
import {useValidator} from "balm-ui";
import GoogleMapAutoComplete from "@/components/shared/GoogleMapAutoComplete";
import GoogleMap from "@/components/shared/GoogleMap";

const validations = {
  first_name: {
    label: 'First Name',
    validator: 'required',
  },
}
export default {
  name: "CustomerAdminCreate",
  components: {GoogleMap, GoogleMapAutoComplete},
  data() {
    return {
      validMsg: {},
      validator: useValidator(),
      validations: validations,
      customer: {
        first_name: "",
        last_name: "",
        company_name: "",
        email: "",
        phone: "",
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
        city: "",
        state: "",
        postal_code: "",
        latitude: "",
        longitude: "",
        contact_same_as_customer: true,
        contacts: [this.addContact()],
      }
    },
    setLocation({location, ...data}) {
      location.address_line_1 = data.address_line_1
      location.name = data.name
      location.latitude = data.latitude
      location.longitude = data.longitude
      location.postal_code = data.postal_code
      location.state = data.state
      location.city = data.city
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

.location {
  display: grid;
  grid-template-areas: "inputs  map"
  "inputs  map"
  "divider  divider"
"contacts contacts";
  justify-items: center;
}

.location-inputs {
  grid-area: inputs;
  align-content: space-evenly;
  justify-content: space-around;
  align-items: center;
  display: grid;
  grid-template-areas: "address-line-1 address-line-1 address-line-1"
"address-line-2 address-line-2 address-line-2"
"city state postal-code";
}

.location-map {
  grid-area: map;
}

.location-divider {
  grid-area: divider;
}

.location-contacts{
  grid-area: contacts;
}

.location-address-line-1 {
  grid-area: address-line-1
}

.location-address-line-2 {
  grid-area: address-line-2
}

.location-city {
  grid-area: city
}

.location-state {
  grid-area: state
}

.location-postal-code {
  grid-area: postal-code
}

</style>