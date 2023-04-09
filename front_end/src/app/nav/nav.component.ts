import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {AuthService} from "../services/auth.service";
import {WebService} from "../services/web.service";
@Component({
 selector: 'navigation',
 templateUrl: './nav.component.html',
 styleUrls: []
})
export class NavComponent {
  isLoggedIn: boolean=true;

  constructor(private router: Router, private authService: AuthService, private webService: WebService) {
    this.isLoggedIn = this.authService.isLoggedIn();
    console.log('Initial isLoggedIn:', this.isLoggedIn); // Add this line to log the initial value
    this.authService.isLoggedIn$.subscribe(isLoggedIn => {
      this.isLoggedIn = isLoggedIn;
      console.log('Updated isLoggedIn:', isLoggedIn); // Add this line to log the updated value
    });
  }

  ngOnInit() {
    this.authService.isLoggedIn$.subscribe(isLoggedIn => {
      this.isLoggedIn = isLoggedIn;
    });
  }

  logout() {
    this.webService.logout()
    this.isLoggedIn = false;
    this.router.navigate(['/']);
  }
}
