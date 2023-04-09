import { Component, OnInit } from '@angular/core';
import { WebService } from '../services/web.service';
import { HttpClient } from '@angular/common/http';
import {AuthService} from "../services/auth.service";

@Component({
  selector: 'profile',
  templateUrl: './profile.component.html',
})
export class ProfileComponent implements OnInit {
  profile: any;
  isAdmin: boolean = false;

  constructor(private webService: WebService, private authService: AuthService) {}

  ngOnInit() {
    this.authService.userData$.subscribe((userData) => {
      if (userData) {
        this.isAdmin = userData.isAdmin;
      } else {
        this.isAdmin = false;
      }
    });

    this.webService.getProfile().subscribe(
      (profile) => {
        this.profile = profile;
      },
      (error) => {
        console.error('Failed to get profile:', error);
      }
    );
  }
}
