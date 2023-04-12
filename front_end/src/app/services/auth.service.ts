import {Injectable} from '@angular/core';
import {BehaviorSubject} from 'rxjs';
import {HttpClient, HttpHeaders} from "@angular/common/http";

@Injectable({
  providedIn: 'root',
})
export class AuthService {

  private _isLoggedIn = new BehaviorSubject<boolean>(this.isLoggedIn());
  public isLoggedIn$ = this._isLoggedIn.asObservable();

  private _userData = new BehaviorSubject<any>(null);

  private _isAdmin = new BehaviorSubject<boolean>(this.getIsAdmin());
  public isAdmin$ = this._isAdmin.asObservable();

  private voter_id: any;
  private gov_id: any;

  constructor(private http: HttpClient) {}

  isLoggedIn(): boolean {
    const token = localStorage.getItem('access_token');

    return !!token;
  }

  getToken() {
    return localStorage.getItem('access_token');
  }

  setUser(userData: any) {
    this._userData.next(userData);
    this.setIsAdmin(userData.isAdmin);
  }

  getGovId(): any {
    return localStorage.getItem('govId');
  }

  public setGovId(gov_id: boolean) {
    this.gov_id = gov_id
    localStorage.setItem('govId', gov_id.toString());

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
    localStorage.setItem('voter_id', voter_id.toString());
  }

  getVoterId(): number | null {
    const voterIdStr = localStorage.getItem('voter_id');
    if (voterIdStr) {
      return parseInt(voterIdStr, 10);
    } else {
      return null;
    }
  }

  resetElection() {
    const headers = new HttpHeaders().set('Authorization', 'Bearer ' + this.getToken());
    return this.http.delete('http://localhost:5000/api/v1.0/votes',{ headers });
  }
}
