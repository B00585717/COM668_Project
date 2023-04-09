import { Component } from '@angular/core';
import { WebService } from '../services/web.service';
import { Router } from '@angular/router';

@Component({
  selector: 'logout',
  template: ''
})
export class LogoutComponent {
  constructor(private webService: WebService, private router: Router) {
    this.webService.logout();
    this.router.navigate(['/login']);
  }
}
