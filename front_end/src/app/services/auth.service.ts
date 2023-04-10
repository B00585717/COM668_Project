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

  private _isAdmin = new BehaviorSubject<boolean>(this.getIsAdmin());
  public isAdmin$ = this._isAdmin.asObservable();

  private user: any;
  private voter_id: any;

  constructor() {}

  isLoggedIn(): boolean {
    const token = localStorage.getItem('access_token');

    return !!token;
  }

  setUser(userData: any) {
    this.user = userData;
    this.setIsAdmin(userData.isAdmin);
  }

  getUser() {
    return this._userData.getValue();
  }

  public setLoggedIn(loggedIn: boolean) {
    this._isLoggedIn.next(loggedIn);
  }

  getIsAdmin(): boolean {
    const isAdmin = localStorage.getItem('isAdmin');
    return isAdmin === 'true';
  }

  public setIsAdmin(isAdmin: boolean) {
    localStorage.setItem('isAdmin', isAdmin.toString());
    this._isAdmin.next(isAdmin);
  }

  setVoterId(voter_id: number) {
    this.voter_id = voter_id;
  }

  // Add a new method to get voter_id
  getVoterId(): number | null {
    return this.voter_id;
  }
}
