import {Component} from "@angular/core";
import {WebService} from "../services/web.service";
import {FormBuilder} from "@angular/forms";
import {VoteService} from "../services/vote.service";
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'candidates',
  templateUrl: './candidates.component.html',
  styleUrls: ['./candidates.component.css']
})

export class CandidatesComponent {

  candidate_list: any = [];
  voter_id: any;

  constructor(public webService: WebService,
              private formBuilder: FormBuilder,
              private voteService: VoteService,
              private authService: AuthService) {}

  ngOnInit() {
    this.candidate_list = this.webService.getCandidates();

    this.authService.isLoggedIn$.subscribe((isLoggedIn) => {
      console.log('Is logged in:', isLoggedIn);
      console.log('Voter ID:', this.authService.getVoterId());
      if (isLoggedIn) {
        this.voter_id = this.authService.getVoterId()
      } else {
        this.voter_id = null;
      }
    });
  }
}
