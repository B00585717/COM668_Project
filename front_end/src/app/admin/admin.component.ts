import {Component} from "@angular/core";
import {WebService} from "../web.service";
import {FormBuilder} from "@angular/forms";
import { ActivatedRoute } from "@angular/router";
import {VoteService} from "../vote.service";
import { AuthService } from '../auth.service';

@Component({
  selector: 'admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})

export class AdminComponent {

  candidate_list: any = [];
  voter_list: any = [];
  party_list: any = [];




  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder, private voteService: VoteService, private authService: AuthService) {

  }

  ngOnInit() {
    this.candidate_list = this.webService.getCandidates();
    this.voter_list = this.webService.getUsers();
    this.party_list = this.webService.getParties();
  }
}
