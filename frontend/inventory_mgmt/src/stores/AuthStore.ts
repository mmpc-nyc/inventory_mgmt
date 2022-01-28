import AuthService from "@/services/AuthService";
import {Commit, MutationTree} from "vuex";
import {User} from "@/models/user";

const user: User = JSON.parse(localStorage.getItem("user") || "{}");
class State {
  user: User = new User(user)

const mutations = <MutationTree<State>>{
  loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    refreshToken(state, accessToken) {
      state.status.loggedIn = true;
      state.user = { ...state.user, access: accessToken };
    },
}

const authStore = {
  namespaced: true,
  state: State,
  actions: {
    login({ commit }: { commit: Commit }, user: User) {
      return AuthService.login(user).then(
        (user) => {
          commit("loginSuccess", user);
          return Promise.resolve(user);
        },
        (error) => {
          commit("loginFailure");
          return Promise.reject(error);
        }
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit("logout");
    },
    refreshToken({ commit }, accessToken) {
      commit("refreshToken", accessToken);
    },
  },
  mutations: mutations,
};

export default authStore;
