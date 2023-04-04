import { Component, OnInit } from '@angular/core';
import { WebService } from './web.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'profile',
  templateUrl: './profile.component.html',
})
export class ProfileComponent implements OnInit {
  profile: any;

  constructor(private webService: WebService) {}

  ngOnInit() {
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
