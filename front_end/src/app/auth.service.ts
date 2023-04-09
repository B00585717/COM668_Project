import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  private _isLoggedIn = new BehaviorSubject<boolean>(this.isLoggedIn());
  public isLoggedIn$ = this._isLoggedIn.asObservable();

  private _userData = new BehaviorSubject<any>(null);
  public userData$ = this._userData.asObservable();

  constructor() {}

  isLoggedIn(): boolean {
    const token = localStorage.getItem('access_token');

    return !!token;
  }

  setUser(userData: any) {
    this._userData.next(userData);
  }

  getUser() {
    return this._userData.getValue();
  }

  public setLoggedIn(loggedIn: boolean) {
    this._isLoggedIn.next(loggedIn);
  }
}
