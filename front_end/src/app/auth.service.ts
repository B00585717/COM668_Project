import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private user: any;

  private _isLoggedIn = new BehaviorSubject<boolean>(this.isLoggedIn());
  public isLoggedIn$ = this._isLoggedIn.asObservable();

  constructor() {}

  isLoggedIn(): boolean {
    const token = localStorage.getItem('access_token');

    if (token) {
      return true;
    } else {
      return false;
    }
  }

  // Call this method when the user logs in
  setUser(userData: any) {
    this.user = userData;
  }

  // Call this method to get the logged-in user's data
  getUser() {
    return this.user;
  }

  public setLoggedIn(loggedIn: boolean) {
    this._isLoggedIn.next(loggedIn);
  }
}
