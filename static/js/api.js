/* ============================================================
   API CLIENT
   ------------------------------------------------------------
   Talks to an "advanced e-commerce" REST backend (Express/Mongo
   style JWT API). Edit API_BASE + the ENDPOINTS map below to
   match your actual backend's routes — every page in this
   project calls through this one file, so that's the only
   place you should need to touch.
   ============================================================ */

const API_BASE = window.API_BASE || "/api";

const ENDPOINTS = {
  register:        "/auth/register",
  login:            "/auth/login",
  logout:           "/auth/logout",
  me:               "/auth/me",
  forgotPassword:   "/auth/forgot-password",

  products:         "/products",
  product: (id) =>  `/products/${id}`,
  categories:       "/categories/",
  reviews: (productId) => `/products/${productId}/reviews`,

  cart:             "/cart",
  cartItem: (id) => `/cart/${id}`,

  orders:           "/orders",
  order: (id) =>    `/orders/${id}`,

  adminStats:       "/admin/stats",
  adminProducts:    "/admin/products",
  adminProduct: (id) => `/admin/products/${id}`,
  adminOrders:      "/admin/orders",
  adminOrder: (id) => `/admin/orders/${id}`,
  adminUsers:       "/admin/users",
};

/* ---------------- token storage ---------------- */
const Auth = {
  getToken(){ return localStorage.getItem("ec_token"); },
  setToken(t){ localStorage.setItem("ec_token", t); },
  clearToken(){ localStorage.removeItem("ec_token"); },
  getUser(){ try{ return JSON.parse(localStorage.getItem("ec_user")); }catch(e){ return null; } },
  setUser(u){ localStorage.setItem("ec_user", JSON.stringify(u)); },
  isLoggedIn(){ return !!Auth.getToken(); },
  isAdmin(){ const u = Auth.getUser(); return !!u && u.role === "admin"; },
  logout(){ Auth.clearToken(); localStorage.removeItem("ec_user"); window.location.href = "login.html"; },
};

/* ---------------- core request wrapper ---------------- */
async function apiRequest(path, { method = "GET", body, auth = true, params } = {}) {
  let url = API_BASE + path;
  if (params) {
    const qs = new URLSearchParams(Object.entries(params).filter(([,v]) => v !== undefined && v !== "" && v !== null));
    const str = qs.toString();
    if (str) url += "?" + str;
  }

  const headers = { "Content-Type": "application/json" };
  if (auth && Auth.getToken()) headers["Authorization"] = `Bearer ${Auth.getToken()}`;

  let res;
  try {
    res = await fetch(url, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (networkErr) {
    throw new Error("Can't reach the API. Is the backend running at " + API_BASE + "?");
  }

  let data = null;
  const text = await res.text();
  try { data = text ? JSON.parse(text) : null; } catch (e) { data = { message: text }; }

  if (!res.ok) {
    if (res.status === 401) Auth.clearToken();
    const message = (data && (data.message || data.error)) || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

/* ---------------- API surface ---------------- */
const Api = {
  // -------- auth --------
  register: (payload) => apiRequest(ENDPOINTS.register, { method: "POST", body: payload, auth: false }),
  login:    (payload) => apiRequest(ENDPOINTS.login,    { method: "POST", body: payload, auth: false }),
  me:       ()        => apiRequest(ENDPOINTS.me,       { method: "GET" }),
  forgotPassword: (email) => apiRequest(ENDPOINTS.forgotPassword, { method: "POST", body: { email }, auth: false }),

  // -------- catalog --------
  getProducts: (params) => apiRequest(ENDPOINTS.products, { method: "GET", auth: false, params }),
  getProduct:  (id)     => apiRequest(ENDPOINTS.product(id), { method: "GET", auth: false }),
  getCategories: ()     => apiRequest(ENDPOINTS.categories, { method: "GET", auth: false }),
  getReviews:  (productId) => apiRequest(ENDPOINTS.reviews(productId), { method: "GET", auth: false }),
  postReview:  (productId, payload) => apiRequest(ENDPOINTS.reviews(productId), { method: "POST", body: payload }),

  // -------- cart --------
  getCart:        () => apiRequest(ENDPOINTS.cart, { method: "GET" }),
  addToCart:      (productId, quantity = 1) => apiRequest(ENDPOINTS.cart, { method: "POST", body: { productId, quantity } }),
  updateCartItem: (itemId, quantity) => apiRequest(ENDPOINTS.cartItem(itemId), { method: "PUT", body: { quantity } }),
  removeCartItem: (itemId) => apiRequest(ENDPOINTS.cartItem(itemId), { method: "DELETE" }),
  clearCart:      () => apiRequest(ENDPOINTS.cart, { method: "DELETE" }),

  // -------- orders / checkout --------
  createOrder: (payload) => apiRequest(ENDPOINTS.orders, { method: "POST", body: payload }),
  getOrders:   ()        => apiRequest(ENDPOINTS.orders, { method: "GET" }),
  getOrder:    (id)      => apiRequest(ENDPOINTS.order(id), { method: "GET" }),

  // -------- admin --------
  getStats:        () => apiRequest(ENDPOINTS.adminStats, { method: "GET" }),
  adminGetProducts:(params) => apiRequest(ENDPOINTS.adminProducts, { method: "GET", params }),
  adminCreateProduct: (payload) => apiRequest(ENDPOINTS.adminProducts, { method: "POST", body: payload }),
  adminUpdateProduct: (id, payload) => apiRequest(ENDPOINTS.adminProduct(id), { method: "PUT", body: payload }),
  adminDeleteProduct: (id) => apiRequest(ENDPOINTS.adminProduct(id), { method: "DELETE" }),
  adminGetOrders:  (params) => apiRequest(ENDPOINTS.adminOrders, { method: "GET", params }),
  adminUpdateOrderStatus: (id, status) => apiRequest(ENDPOINTS.adminOrder(id), { method: "PUT", body: { status } }),
  adminGetUsers:   (params) => apiRequest(ENDPOINTS.adminUsers, { method: "GET", params }),
};

/* ---------------- toast helper (used on every page) ---------------- */
function ensureToastStack() {
  let stack = document.getElementById("toast-stack");
  if (!stack) {
    stack = document.createElement("div");
    stack.id = "toast-stack";
    document.body.appendChild(stack);
  }
  return stack;
}
function toast(message, type = "info", ms = 3200) {
  const stack = ensureToastStack();
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = message;
  stack.appendChild(el);
  setTimeout(() => el.remove(), ms);
}

/* ---------------- small formatting helpers ---------------- */
function money(n) {
  const num = Number(n || 0);
  return "$" + num.toFixed(2);
}
function qs(sel, root = document) { return root.querySelector(sel); }
function qsa(sel, root = document) { return Array.from(root.querySelectorAll(sel)); }

/* ---------------- shared header state (cart count, auth links) ---------------- */
async function refreshHeaderState() {
  const cartCountEl = qs("[data-cart-count]");
  const authSlot = qs("[data-auth-slot]");

  if (authSlot) {
    if (Auth.isLoggedIn()) {
      const user = Auth.getUser();
      authSlot.innerHTML = `
        <a class="icon-link" href="profile.html">👤 ${user?.name ? user.name.split(" ")[0] : "Account"}</a>
        <button class="icon-link" id="logoutBtn" type="button">Logout</button>
      `;
      const logoutBtn = qs("#logoutBtn");
      if (logoutBtn) logoutBtn.addEventListener("click", () => Auth.logout());
    } else {
      authSlot.innerHTML = `<a class="icon-link" href="login.html">👤 Login</a>`;
    }
  }

  if (cartCountEl) {
    if (!Auth.isLoggedIn()) {
      cartCountEl.textContent = "0";
      return;
    }
    try {
      const cart = await Api.getCart();
      const count = (cart.items || cart.cartItems || []).reduce((sum, it) => sum + (it.quantity || 1), 0);
      cartCountEl.textContent = count;
    } catch (e) { /* silent — header shouldn't break the page */ }
  }
}

document.addEventListener("DOMContentLoaded", refreshHeaderState);