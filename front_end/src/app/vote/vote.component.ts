import {Component} from "@angular/core";
import {WebService} from "../services/web.service";
import {FormBuilder} from "@angular/forms";
import {ActivatedRoute, Router} from "@angular/router";
import {VoteService} from "../services/vote.service";
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'vote',
  templateUrl: './vote.component.html',
  styleUrls: ['./vote.component.css']
})

export class VoteComponent {

  candidate_list: any = [];
  voter_id: any;

  remaining_positive_votes: any;
  remaining_negative_votes: any;

  constructor(public webService: WebService,
              private formBuilder: FormBuilder,
              private voteService: VoteService,
              private authService: AuthService,
              private router: Router) {}

submitVote(vote_type: number, candidate: any) {
  this.voteService.voteForCandidate(this.voter_id, candidate.candidate_id, vote_type).subscribe(
    response => {
      console.log('Vote submitted', response);
      this.updateRemainingVotes();
      this.voteService.getRemainingVotes(this.voter_id).subscribe(remainingVotes => {
        console.log('Remaining Votes:', remainingVotes);
        if (remainingVotes.remaining_positive_votes === 0 && remainingVotes.remaining_negative_votes === 0) {
          this.router.navigate(['/voting-data']);
        }
      });

    },
    error => console.error('Error submitting vote', error)
  );
}

  onVoteButtonClick(vote_type: number, candidate: any) {
    this.submitVote(vote_type, candidate);
  }

  ngOnInit() {
    this.candidate_list = this.webService.getCandidates();

    this.authService.isLoggedIn$.subscribe((isLoggedIn) => {
      console.log('Is logged in:', isLoggedIn);
      console.log('Voter ID:', this.authService.getVoterId());
      if (isLoggedIn) {
        this.voter_id = this.authService.getVoterId()
        this.updateRemainingVotes();
      } else {
        this.voter_id = null;
      }
    });
  }

    updateRemainingVotes() {
    this.voteService.getRemainingVotes(this.voter_id).subscribe(response => {
      this.remaining_positive_votes = response.remaining_positive_votes;
      this.remaining_negative_votes = response.remaining_negative_votes;
    });
  }
}


