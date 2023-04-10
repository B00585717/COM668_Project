import {Component} from "@angular/core";
import {WebService} from "../services/web.service";
import {FormBuilder} from "@angular/forms";
import {ActivatedRoute, Router} from "@angular/router";
import {VoteService} from "../services/vote.service";
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'candidates',
  templateUrl: './candidates.component.html',
  styleUrls: ['./candidates.component.css']
})

export class CandidatesComponent {

  candidate_list: any = [];
  candidate_form: any;
  voter_id: any;

  constructor(public webService: WebService,
              private formBuilder: FormBuilder,
              private voteService: VoteService,
              private authService: AuthService,
              private router: Router) {}

  onVoteButtonClick(candidate_id: number) {
    console.log('Voter ID:', this.voter_id);
    console.log('Candidate ID:', candidate_id);
    this.voteService.voteForCandidate(this.voter_id, candidate_id).subscribe(
      response => {console.log('Vote submitted', response)
      this.router.navigate(['/voting-data']);
        },
      error => console.error('Error submitting vote', error)
    );
  }

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

  onSubmit() {
    this.webService.addCandidate(this.candidate_form.value).subscribe((response: any) => {
      this.candidate_form.reset();
    });

    this.candidate_form = this.formBuilder.group({
      candidate_firstname: '',
      candidate_lastname: '',
      party_id: '',
      image: '',
      constituency_id: '',
      statement:'',
    });
  }
}
