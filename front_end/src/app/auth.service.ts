import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private user: any;

  constructor() {}

  // Call this method when the user logs in
  setUser(userData: any) {
    this.user = userData;
  }

  // Call this method to get the logged-in user's data
  getUser() {
    return this.user;
  }
}
